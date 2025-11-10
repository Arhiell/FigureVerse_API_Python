import hmac
import hashlib
from typing import Optional


def verify_hmac_sha256(secret: str, body: bytes, signature: Optional[str]) -> bool:
    """
    Verifica firma HMAC-SHA256 sobre el cuerpo raw.

    - signature puede venir como "sha256=<hex>" o solo "<hex>".
    - Comparación segura con compare_digest.
    """
    if not signature:
        return False

    sig = signature.strip()
    if sig.startswith("sha256="):
        sig = sig.split("=", 1)[1]

    mac = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, sig)