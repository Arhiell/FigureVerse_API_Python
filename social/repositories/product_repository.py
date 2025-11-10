"""
Repositorio de productos contra la API Core (Node).

Responsable de consumir endpoints públicos de catálogo. No persiste datos,
solo obtiene información por HTTP.
"""

import time
import logging
import requests
from typing import List, Dict, Any
from django.conf import settings


logger = logging.getLogger(__name__)


class ProductRepository:
    """
    Acceso a productos del catálogo en la API Core (Node).
    """

    @staticmethod
    def get_all_products() -> List[Dict[str, Any]]:
        """
        Devuelve la lista completa/paginada de productos. Este método puede
        ajustarse para parámetros de paginación cuando estén definidos.
        """
        base_url = getattr(settings, 'NODE_API_URL', getattr(settings, 'NODE_API_BASE_URL', 'http://localhost:3000'))
        url = f"{base_url}/productos"
        start = time.time()
        resp = requests.get(url, timeout=settings.NODE_API_TIMEOUT)
        duration = (time.time() - start) * 1000
        logger.info("GET %s -> %s (%.2fms)", url, resp.status_code, duration)
        resp.raise_for_status()
        data = resp.json()
        # Asumimos que la API retorna una lista directa; si fuese paginada
        # con metadatos, aquí transformamos a la estructura esperada.
        return data if isinstance(data, list) else data.get('items', [])

    @staticmethod
    def get_product(product_id: int) -> Dict[str, Any]:
        """
        Devuelve el detalle del producto por ID.
        """
        base_url = getattr(settings, 'NODE_API_URL', getattr(settings, 'NODE_API_BASE_URL', 'http://localhost:3000'))
        url = f"{base_url}/productos/{product_id}"
        start = time.time()
        resp = requests.get(url, timeout=settings.NODE_API_TIMEOUT)
        duration = (time.time() - start) * 1000
        logger.info("GET %s -> %s (%.2fms)", url, resp.status_code, duration)
        resp.raise_for_status()
        return resp.json()