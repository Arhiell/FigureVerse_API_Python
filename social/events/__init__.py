"""
Eventos oficiales provenientes de la API Node.

Este paquete define los modelos Pydantic que describen los payloads
publicados en Firestore. Django los consumirá vía Cloud Functions
en fases posteriores.
"""

from .contract_v1 import (
    EventType,
    EventEnvelope,
    UserAuthenticatedEvent,
    UserRegisteredEvent,
    ProductCreatedEvent,
    ProductUpdatedEvent,
    OrderItem,
    OrderCreatedEvent,
    PaymentApprovedEvent,
    InvoiceIssuedEvent,
    ShipmentCreatedEvent,
    DiscountAppliedEvent,
    CompanySettingsUpdatedEvent,
    validate_envelope,
)

__all__ = [
    'EventType',
    'EventEnvelope',
    'UserAuthenticatedEvent',
    'UserRegisteredEvent',
    'ProductCreatedEvent',
    'ProductUpdatedEvent',
    'OrderItem',
    'OrderCreatedEvent',
    'PaymentApprovedEvent',
    'InvoiceIssuedEvent',
    'ShipmentCreatedEvent',
    'DiscountAppliedEvent',
    'CompanySettingsUpdatedEvent',
    'validate_envelope',
]