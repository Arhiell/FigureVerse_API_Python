"""
Repositorio de órdenes/pedidos contra la API Core (Node).

Responsable de obtener colecciones de órdenes, incluyendo sus ítems, para
analítica. No persiste datos en Django; solo lectura por HTTP.
"""

import time
import logging
import requests
from typing import List, Dict, Any
from django.conf import settings


logger = logging.getLogger(__name__)


class OrderRepository:
    """
    Acceso a pedidos en la API Core (Node).
    """

    @staticmethod
    def get_orders() -> List[Dict[str, Any]]:
        """
        Devuelve la colección de órdenes con sus ítems.
        Se asume que cada orden incluye una lista `items` con al menos:
        product_id, quantity y unit_price/price.
        """
        base_url = getattr(settings, 'NODE_API_URL', getattr(settings, 'NODE_API_BASE_URL', 'http://localhost:3000'))
        url = f"{base_url}/orders"
        start = time.time()
        try:
            resp = requests.get(url, timeout=settings.NODE_API_TIMEOUT)
            duration = (time.time() - start) * 1000
            logger.info("GET %s -> %s (%.2fms)", url, resp.status_code, duration)
            resp.raise_for_status()
        except requests.Timeout:
            logger.error("Timeout al consultar órdenes en %s", url)
            raise
        except requests.RequestException as exc:
            logger.error("Error al consultar órdenes: %s", exc)
            raise

        data = resp.json()
        return data if isinstance(data, list) else data.get('items', [])