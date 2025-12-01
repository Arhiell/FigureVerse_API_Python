import requests
import certifi
from django.conf import settings

BASE_URL = settings.CLOUD_FUNCTIONS_BASE_URL
FALLBACK_BASE_URL = getattr(settings, "CLOUD_FUNCTIONS_FALLBACK_BASE_URL", None)
EMULATOR_BASE_URL = getattr(settings, "CLOUD_FUNCTIONS_EMULATOR_BASE_URL", None)
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


def _compose_url(base: str, path: str):
    base_trimmed = base.rstrip("/")
    return f"{base_trimmed}{path}"


def _get_json(path: str):
    bases = []
    if EMULATOR_BASE_URL:
        bases.append(EMULATOR_BASE_URL)
    bases.append(BASE_URL)
    if FALLBACK_BASE_URL:
        bases.append(FALLBACK_BASE_URL)

    last_exc = None
    for base in bases:
        url = _compose_url(base, path)
        is_emulator = base.startswith("http://localhost:") or base.startswith("http://127.0.0.1:")
        verify = False if is_emulator else (certifi.where() if VERIFY_TLS else False)
        try:
            response = requests.get(url, headers=_headers(), timeout=TIMEOUT, verify=verify, allow_redirects=True)
            if 500 <= response.status_code < 600:
                raise requests.HTTPError(response=response)
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.SSLError, requests.HTTPError) as e:
            last_exc = e
            continue

    raise CloudFunctionsError(str(last_exc) if last_exc else "Unknown error calling Cloud Functions")


def get_products():
    return _get_json(f"{PREFIX}/productos")


def get_reviews():
    return _get_json(f"{PREFIX}/resenas")


def get_all_reviews():
    return _get_json(f"{PREFIX}/resenas")


def get_reviews_by_product(product_id):
    return _get_json(f"{PREFIX}/resenas/producto/{product_id}")
