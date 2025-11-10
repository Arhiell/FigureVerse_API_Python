"""
Autenticación DRF que valida el JWT emitido por la API de Node.

- Extrae el encabezado Authorization (Bearer <token>).
- Llama a /auth/profile en Node para validar el token.
- Si es válido, retorna un objeto de usuario ligero y el token.
"""

from typing import Optional, Tuple
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser

from social.services import node_client


class LightweightUser:
    """
    Usuario ligero usado solo para request.user en vistas protegidas.
    No se persiste en la base local; proviene de la API de Node.
    """

    def __init__(self, user_id: str, email: str, role: str):
        self.id = user_id
        self.email = email
        self.role = role
        self.is_authenticated = True

    def __str__(self) -> str:
        return f"LightweightUser(id={self.id}, role={self.role})"


class NodeJWTAuthentication(BaseAuthentication):
    """
    Clase de autenticación para DRF que valida tokens contra la API de Node.
    """

    keyword = "Bearer"

    def authenticate(self, request) -> Optional[Tuple[LightweightUser, str]]:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            # No hay encabezado de autorización: DRF continuará y marcará la vista
            # como no autenticada si se requiere permiso.
            return None

        try:
            keyword, token = auth_header.split(" ", 1)
        except ValueError:
            raise AuthenticationFailed("Encabezado Authorization inválido")

        if keyword != self.keyword or not token:
            raise AuthenticationFailed("Formato de Authorization no soportado")

        try:
            profile = node_client.get_profile(token)
        except Exception as exc:
            # Errores 401/403/5xx quedan mapeados a autenticación fallida.
            raise AuthenticationFailed(f"Token inválido o no verificado: {exc}")

        # Se espera que profile incluya id, email y role.
        user_id = str(profile.get("id") or profile.get("_id") or "")
        email = profile.get("email") or ""
        role = profile.get("role") or ""

        if not user_id:
            # Si la API no devolvió id, no autenticamos.
            raise AuthenticationFailed("Perfil inválido: falta id de usuario")

        user = LightweightUser(user_id=user_id, email=email, role=role)
        return (user, token)