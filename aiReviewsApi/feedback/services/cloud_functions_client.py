import requests
import certifi
from django.conf import settings

BASE_URL = settings.CLOUD_FUNCTIONS_BASE_URL
FALLBACK_BASE_URL = getattr(settings, "CLOUD_FUNCTIONS_FALLBACK_BASE_URL", None)
TIMEOUT = getattr(settings, "CLOUD_FUNCTIONS_TIMEOUT", 10)
AUTH_TOKEN = getattr(settings, "CLOUD_FUNCTIONS_AUTH_TOKEN", None)
FN = getattr(settings, "CLOUD_FUNCTIONS_FUNCTION_NAME", "api")
PREFIX = f"/{FN}" if FN else ""
VERIFY_TLS = getattr(settings, "CLOUD_FUNCTIONS_VERIFY_TLS", True)


class CloudFunctionsError(Exception):
    pass


def _headers():
    h = {}
    if AUTH_TOKEN:
        h["Authorization"] = f"Bearer {AUTH_TOKEN}"
    h["User-Agent"] = "FigureVerseAPI/1.0"
    h["Connection"] = "close"
    h["Accept"] = "application/json"
    return h


def _get_json(path: str):
    url = f"{BASE_URL}{path}"
    verify = certifi.where() if VERIFY_TLS else False
    try:
        response = requests.get(url, headers=_headers(), timeout=TIMEOUT, verify=verify, allow_redirects=True)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        if FALLBACK_BASE_URL:
            fb_url = f"{FALLBACK_BASE_URL}{path}"
            response = requests.get(fb_url, headers=_headers(), timeout=TIMEOUT, verify=verify, allow_redirects=True)
            response.raise_for_status()
            return response.json()
        raise


def get_products():
    return _get_json(f"{PREFIX}/productos")


def get_reviews():
    return _get_json(f"{PREFIX}/resenas")


def get_all_reviews():
    return _get_json(f"{PREFIX}/resenas")


def get_reviews_by_product(product_id):
    return _get_json(f"{PREFIX}/resenas/producto/{product_id}")
