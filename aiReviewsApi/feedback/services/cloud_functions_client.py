import requests
from django.conf import settings

BASE_URL = settings.CLOUD_FUNCTIONS_BASE_URL

def get_products():
    url = f"{BASE_URL}/api/productos"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_reviews():
    url = f"{BASE_URL}/api/resenas"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_reviews_by_product(product_id):
    url = f"{BASE_URL}/api/resenas/producto/{product_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
