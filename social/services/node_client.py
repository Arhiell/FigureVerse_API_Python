"""
Cliente HTTP reutilizable para integrar con la API de Node.

Este módulo centraliza las llamadas y el manejo de errores. Todas las
funciones están comentadas para facilitar el mantenimiento.
"""

import requests
from typing import Optional, Dict, Any
from django.conf import settings


DEFAULT_TIMEOUT_SECONDS = getattr(settings, 'NODE_API_TIMEOUT', 5)


def _auth_header(token: Optional[str]) -> Dict[str, str]:
    """
    Construye el encabezado Authorization si hay token.
    """
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def get_profile(token: str) -> Dict[str, Any]:
    """
    Obtiene el perfil del usuario autenticado desde Node.
    Levanta HTTPError si la respuesta es distinta de 2xx.
    """
    url = f"{settings.NODE_API_BASE_URL}/auth/profile"
    resp = requests.get(url, headers=_auth_header(token), timeout=DEFAULT_TIMEOUT_SECONDS)
    resp.raise_for_status()
    return resp.json()


def get_product(product_id: int, token: Optional[str] = None) -> Dict[str, Any]:
    """
    Obtiene los datos del producto por ID desde Node.
    Levanta HTTPError si la respuesta es distinta de 2xx.
    """
    url = f"{settings.NODE_API_BASE_URL}/productos/{product_id}"
    resp = requests.get(url, headers=_auth_header(token), timeout=DEFAULT_TIMEOUT_SECONDS)
    resp.raise_for_status()
    return resp.json()