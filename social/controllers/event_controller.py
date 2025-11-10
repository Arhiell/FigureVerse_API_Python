"""
Controlador interno de eventos.

Despacha eventos del envelope v1 hacia servicios ligeros. Evita trabajos
pesados dentro de la solicitud: se registran métricas y se prepara
procesamiento asíncrono a futuro.
"""

import logging
from typing import Dict, Any

from social.events import EventType
from social.services.event_processor_service import EventProcessorService


logger = logging.getLogger(__name__)


class InternalEventController:
    """
    Mapea tipos de evento a handlers internos. Actualmente los handlers
    son livianos (logging/contadores). La lógica pesada se delegará a
    pipelines asíncronos en próximos módulos.
    """

    @staticmethod
    def handle(event_type: EventType, payload: Dict[str, Any]) -> None:
        # Registro general
        logger.info("InternalEvent: %s payload_keys=%s", event_type.value, list(payload.keys()))

        # Dispatch hacia el servicio de procesamiento
        if event_type == EventType.OrderCreated:
            EventProcessorService.on_order_created(payload)
        elif event_type == EventType.PaymentApproved:
            EventProcessorService.on_payment_approved(payload)
        elif event_type == EventType.ProductCreated:
            EventProcessorService.on_product_created(payload)
        elif event_type == EventType.ProductUpdated:
            EventProcessorService.on_product_updated(payload)
        elif event_type == EventType.UserAuthenticated:
            EventProcessorService.on_user_authenticated(payload)
        elif event_type == EventType.CompanySettingsUpdated:
            EventProcessorService.on_company_settings_updated(payload)
        else:
            # Eventos no mapeados en esta fase: solo registro
            logger.debug("Evento no mapeado: %s", event_type.value)

    # Los handlers internos se delegan al EventProcessorService