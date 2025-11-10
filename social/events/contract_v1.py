"""
Contrato JSON v1 unificado para eventos Node → Firebase → Django.

Define:
- EventType: catálogo de eventos oficiales
- Origin: metadatos del origen
- EventEnvelope v1: estructura estándar con `event`, `version`, `timestamp`, `origin`, `payload`
- Modelos Pydantic de payload por cada evento
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel, Field, EmailStr, field_validator


class EventType(str, Enum):
    UserAuthenticated = "UserAuthenticated"
    UserRegistered = "UserRegistered"
    ProductCreated = "ProductCreated"
    ProductUpdated = "ProductUpdated"
    OrderCreated = "OrderCreated"
    PaymentApproved = "PaymentApproved"
    InvoiceIssued = "InvoiceIssued"
    ShipmentCreated = "ShipmentCreated"
    DiscountApplied = "DiscountApplied"
    CompanySettingsUpdated = "CompanySettingsUpdated"


class Origin(BaseModel):
    service: str = Field(default="node-core")
    environment: str
    ip: str

    @field_validator("service")
    @classmethod
    def _ensure_node_core(cls, v: str) -> str:
        if v != "node-core":
            raise ValueError("origin.service debe ser siempre 'node-core'")
        return v


class EventEnvelope(BaseModel):
    """
    Envelope estándar v1:
    {
      "event": "NombreDelEvento",
      "version": "v1",
      "timestamp": ISO8601,
      "origin": { "service": "node-core", "environment": "...", "ip": "..." },
      "payload": { ... }
    }
    """

    event: EventType
    version: str = Field(default="v1")
    timestamp: datetime
    origin: Origin
    payload: Dict[str, Any]

    @field_validator("version")
    @classmethod
    def _ensure_v1(cls, v: str) -> str:
        if v != "v1":
            raise ValueError("version debe ser 'v1'")
        return v

    def parse_payload(self) -> BaseModel:
        schema = EVENT_SCHEMA_BY_TYPE[self.event]
        return schema.model_validate(self.payload)


# Payloads por evento

# 1) UserAuthenticated
class UserAuthenticatedEvent(BaseModel):
    user_id: str
    email: EmailStr
    rol: str


# 2) UserRegistered
class Perfil(BaseModel):
    nombre: str
    direccion: str
    telefono: str


class UserRegisteredEvent(BaseModel):
    user_id: str
    email: EmailStr
    rol: str
    perfil: Optional[Perfil] = None


# 3) ProductCreated
class ProductCreatedEvent(BaseModel):
    product_id: int
    nombre: str
    precio: Decimal
    stock: int
    categoria_id: int
    fabricante_id: int
    universo_id: int


# 4) ProductUpdated
class ProductUpdatedEvent(BaseModel):
    product_id: int
    cambios: Dict[str, Any] = Field(default_factory=dict)


# 5) OrderCreated
class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: Decimal


class OrderCreatedEvent(BaseModel):
    order_id: int
    user_id: str
    items: List[OrderItem]
    total: Decimal
    estado: str


# 6) PaymentApproved
class PaymentApprovedEvent(BaseModel):
    payment_id: str
    order_id: int
    monto: Decimal
    metodo: str


# 7) InvoiceIssued
class InvoiceIssuedEvent(BaseModel):
    invoice_id: str
    order_id: int
    total: Decimal
    metodo_pago: str


# 8) ShipmentCreated
class ShipmentCreatedEvent(BaseModel):
    shipment_id: str
    order_id: int
    direccion: str
    estado: str


# 9) DiscountApplied
class DiscountAppliedEvent(BaseModel):
    order_id: int
    codigo: str
    valor: Decimal


# 10) CompanySettingsUpdated
class CompanySettingsUpdatedEvent(BaseModel):
    previo: Dict[str, Any]
    nuevo: Dict[str, Any]


# Mapeo para validación dinámica
EVENT_SCHEMA_BY_TYPE: Dict[EventType, Type[BaseModel]] = {
    EventType.UserAuthenticated: UserAuthenticatedEvent,
    EventType.UserRegistered: UserRegisteredEvent,
    EventType.ProductCreated: ProductCreatedEvent,
    EventType.ProductUpdated: ProductUpdatedEvent,
    EventType.OrderCreated: OrderCreatedEvent,
    EventType.PaymentApproved: PaymentApprovedEvent,
    EventType.InvoiceIssued: InvoiceIssuedEvent,
    EventType.ShipmentCreated: ShipmentCreatedEvent,
    EventType.DiscountApplied: DiscountAppliedEvent,
    EventType.CompanySettingsUpdated: CompanySettingsUpdatedEvent,
}


def validate_envelope(event: EventType, payload: Dict[str, Any]) -> BaseModel:
    """Valida un payload según el tipo y retorna la instancia tipada."""
    schema = EVENT_SCHEMA_BY_TYPE[event]
    return schema.model_validate(payload)