"""
Servicio de Procesamiento de Eventos (Módulo 6D)

Responsable de transformar eventos del contrato v1 en acciones de negocio:
- actualizar métricas/pre-agregados locales (ProductAnalytics)
- invalidar/actualizar cachés
- registrar actividad ligera

Las operaciones pesadas se delegarán a pipelines asíncronos en módulos futuros.
"""

import logging
from decimal import Decimal
from typing import Dict, Any, List

from django.db import transaction

try:
    # Modelo opcional; puede no existir si no se migró todavía
    from social.models.analytics import ProductAnalytics  # type: ignore
except Exception:
    ProductAnalytics = None  # type: ignore

from social.services.product_cache import ProductCacheService


logger = logging.getLogger(__name__)


class EventProcessorService:
    """
    Implementa handlers por tipo de evento del contrato v1.
    """

    @staticmethod
    def _items_from_order(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        items = payload.get('items') or []
        normalized = []
        for item in items:
            pid = item.get('product_id') or (item.get('product') or {}).get('id')
            qty = item.get('quantity') or item.get('qty')
            price = item.get('unit_price') or item.get('price')
            if pid is None or qty is None or price is None:
                continue
            normalized.append({'product_id': int(pid), 'quantity': int(qty), 'unit_price': Decimal(str(price))})
        return normalized

    @staticmethod
    def on_order_created(payload: Dict[str, Any]) -> None:
        """Actualiza agregados por producto a partir de los ítems del pedido."""
        items = EventProcessorService._items_from_order(payload)
        if not items:
            logger.debug("OrderCreated sin items; order_id=%s", payload.get('order_id'))
            return

        if ProductAnalytics is None:
            # Sin modelo persistente: registramos en log y salimos
            total = sum(i['quantity'] * float(i['unit_price']) for i in items)
            logger.info("OrderCreated (no persist): order_id=%s total=%.2f items=%d",
                        payload.get('order_id'), total, len(items))
            return

        with transaction.atomic():
            for item in items:
                pa, _created = ProductAnalytics.objects.select_for_update().get_or_create(
                    product_id=item['product_id'], defaults={'total_sales': 0, 'total_revenue': Decimal('0.00')}
                )
                pa.total_sales += item['quantity']
                pa.total_revenue = (pa.total_revenue or Decimal('0.00')) + (item['unit_price'] * item['quantity'])
                pa.save()
        logger.debug("OrderCreated: agregados actualizados para %d productos", len(items))

    @staticmethod
    def on_payment_approved(payload: Dict[str, Any]) -> None:
        """Registra ingresos confirmados a nivel log; persistencia futura opcional."""
        monto = payload.get('monto')
        order_id = payload.get('order_id')
        try:
            amt = float(monto) if monto is not None else 0.0
        except Exception:
            amt = 0.0
        logger.info("PaymentApproved: order_id=%s monto=%.2f", order_id, amt)

    @staticmethod
    def on_product_created(payload: Dict[str, Any]) -> None:
        """Cachea metadatos básicos del producto para acelerar lecturas locales."""
        pid = payload.get('product_id')
        if pid is None:
            return
        ProductCacheService.set(int(pid), {
            'nombre': payload.get('nombre'),
            'precio': payload.get('precio'),
            'stock': payload.get('stock'),
            'categoria_id': payload.get('categoria_id'),
            'fabricante_id': payload.get('fabricante_id'),
            'universo_id': payload.get('universo_id'),
        })
        logger.debug("ProductCreated: cache actualizado product_id=%s", pid)

    @staticmethod
    def on_product_updated(payload: Dict[str, Any]) -> None:
        """Invalida cache del producto y deja registro de cambios."""
        pid = payload.get('product_id')
        if pid is None:
            return
        ProductCacheService.invalidate(int(pid))
        cambios = list((payload.get('cambios') or {}).keys())
        logger.info("ProductUpdated: product_id=%s cambios=%s", pid, cambios)

    @staticmethod
    def on_user_authenticated(payload: Dict[str, Any]) -> None:
        """Registra actividad de inicio de sesión del usuario."""
        logger.debug("UserAuthenticated: user_id=%s email=%s", payload.get('user_id'), payload.get('email'))

    @staticmethod
    def on_company_settings_updated(payload: Dict[str, Any]) -> None:
        """Registra compare básico de settings; persistencia futura opcional."""
        before_keys = list((payload.get('previo') or {}).keys()) or list((payload.get('before') or {}).keys())
        after_keys = list((payload.get('nuevo') or {}).keys()) or list((payload.get('after') or {}).keys())
        logger.info("CompanySettingsUpdated: before=%s after=%s", before_keys, after_keys)