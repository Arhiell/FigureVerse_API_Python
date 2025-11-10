"""
Esquemas oficiales de eventos enviados por la API Node a Firestore.

Estos modelos Pydantic constituyen el contrato entre Node y Django.
Cloud Functions leerá documentos, y Django validará con estos esquemas.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union

from pydantic import BaseModel, Field, EmailStr


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


# 1) UserAuthenticated
class UserAuthenticatedEvent(BaseModel):
    user_id: str
    email: EmailStr
    timestamp: datetime
    rol: str


# 2) UserRegistered
class UserRegisteredEvent(BaseModel):
    user_id: str
    email: EmailStr
    rol: str
    profile_data: Optional[Dict[str, Any]] = None


# 3) ProductCreated
class ProductCreatedEvent(BaseModel):
    product_id: int
    nombre: str
    precio: Decimal
    stock: int
    categoria: str
    fabricante: str
    universo: str


# 4) ProductUpdated
class ProductUpdatedEvent(BaseModel):
    product_id: int
    # Campos modificados (nombre, precio, stock, etc.)
    cambios: Dict[str, Any] = Field(default_factory=dict)


# 5) OrderCreated
class OrderItem(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal


class OrderCreatedEvent(BaseModel):
    order_id: str
    user_id: str
    items: List[OrderItem]
    total: Decimal
    estado: str


# 6) PaymentApproved
class PaymentApprovedEvent(BaseModel):
    payment_id: str
    order_id: str
    metodo: str
    monto: Decimal


# 7) InvoiceIssued
class InvoiceIssuedEvent(BaseModel):
    invoice_id: str
    order_id: str
    total: Decimal
    metodo: str


# 8) ShipmentCreated
class ShipmentCreatedEvent(BaseModel):
    shipment_id: str
    order_id: str
    direccion: str
    estado: str


# 9) DiscountApplied
class DiscountAppliedEvent(BaseModel):
    order_id: str
    codigo_descuento: str
    valor: Decimal


# 10) CompanySettingsUpdated
class CompanySettingsUpdatedEvent(BaseModel):
    before: Dict[str, Any]
    after: Dict[str, Any]


# Mapeo de tipo -> esquema para validación dinámica
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


class EventEnvelope(BaseModel):
    """
    Envoltura estándar para documentos en Firestore.

    - type: tipo del evento oficial.
    - payload: objeto JSON que debe cumplir el esquema según type.
    - emitted_at: fecha/hora de emisión (servidor Node).
    - source: origen del evento (por defecto 'node_api').
    """

    type: EventType
    payload: Dict[str, Any]
    emitted_at: datetime = Field(default_factory=datetime.utcnow)
    source: str = Field(default="node_api")

    def parse_payload(self) -> BaseModel:
        """
        Valida y retorna el payload como modelo Pydantic del tipo correspondiente.
        """
        schema = EVENT_SCHEMA_BY_TYPE[self.type]
        return schema.model_validate(self.payload)


def validate_envelope(event_type: EventType, payload: Dict[str, Any]) -> BaseModel:
    """
    Valida un payload dado su tipo y retorna la instancia tipada.
    Útil para Cloud Functions o consumidores que reciben documentos JSON.
    """
    schema = EVENT_SCHEMA_BY_TYPE[event_type]
    return schema.model_validate(payload)