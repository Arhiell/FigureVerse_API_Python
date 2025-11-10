"""
Endpoint interno /internal/events

Características:
- Solo comunicación servicio→servicio (Cloud Functions → Django)
- Verificación HMAC-SHA256 con secreto compartido
- Validación del contrato v1 y despacho a controlador interno
- Respuesta rápida y mínima
"""

import json
import logging
from typing import Any, Dict

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from social.utils.hmac import verify_hmac_sha256
from social.events import EventEnvelope, EventType
from social.controllers.event_controller import InternalEventController
from pydantic import ValidationError


logger = logging.getLogger(__name__)


class InternalEventsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # 1) Leer cuerpo raw
        body_bytes = request.body or b""

        # 2) Verificar firma HMAC
        signature = request.headers.get('X-Internal-Events-Signature') or request.headers.get('X-Signature')
        secret = getattr(settings, 'INTERNAL_EVENTS_SECRET', None)
        if not secret:
            logger.error('INTERNAL_EVENTS_SECRET no configurado')
            return Response({'ok': False, 'error': 'misconfigured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not verify_hmac_sha256(secret, body_bytes, signature):
            return Response({'ok': False}, status=status.HTTP_401_UNAUTHORIZED)

        # 3) Parsear JSON y validar envelope v1
        try:
            payload_json: Dict[str, Any] = json.loads(body_bytes.decode('utf-8'))
        except json.JSONDecodeError:
            return Response({'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            env = EventEnvelope.model_validate(payload_json)
        except ValidationError as exc:
            # Si el evento no es reconocido (compatibilidad hacia adelante), ignorar
            logger.info('Envelope inválido o evento desconocido: %s', exc.errors())
            return Response({'ok': True}, status=status.HTTP_200_OK)

        # 4) Despachar a controlador (liviano)
        try:
            typed_payload = env.parse_payload()
            InternalEventController.handle(env.event, typed_payload.model_dump())
        except Exception as exc:
            # Evitar retries masivos; responder 200 y loguear el error
            logger.error('Error procesando evento %s: %s', env.event.value, exc)
            return Response({'ok': True}, status=status.HTTP_200_OK)

        # 5) Respuesta mínima
        return Response({'ok': True}, status=status.HTTP_200_OK)