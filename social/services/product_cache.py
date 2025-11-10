"""
Servicio secundario de caché de productos.

Mantiene un caché en memoria con metadatos básicos del producto para
evitar llamadas innecesarias mientras se procesan eventos.
"""

from typing import Dict, Any, Optional


_CACHE: Dict[int, Dict[str, Any]] = {}


class ProductCacheService:
    @staticmethod
    def set(product_id: int, data: Dict[str, Any]) -> None:
        _CACHE[product_id] = data

    @staticmethod
    def get(product_id: int) -> Optional[Dict[str, Any]]:
        return _CACHE.get(product_id)

    @staticmethod
    def invalidate(product_id: int) -> None:
        _CACHE.pop(product_id, None)

    @staticmethod
    def clear() -> None:
        _CACHE.clear()