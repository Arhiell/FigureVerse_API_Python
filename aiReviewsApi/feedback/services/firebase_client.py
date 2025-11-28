from datetime import datetime
from django.conf import settings


COLLECTION_NAME = "product_analysis"


def _get_collection():
    """
    Devuelve la referencia a la colección de análisis en Firestore.
    Requiere que en settings.py se haya inicializado FIRESTORE_DB.
    """
    return settings.FIRESTORE_DB.collection(COLLECTION_NAME)


def save_product_analysis(product_id, analysis_data: dict):
    """
    Guarda (o actualiza) el análisis de un producto en Firestore.

    - product_id: ID del producto (int o str)
    - analysis_data: diccionario con los campos del análisis
    """
    doc_ref = _get_collection().document(str(product_id))

    # Siempre agregamos/actualizamos la fecha de último análisis
    analysis_data["last_analyzed_at"] = datetime.utcnow().isoformat() + "Z"

    # Usamos merge=True para no sobreescribir campos que no están en analysis_data
    doc_ref.set(analysis_data, merge=True)


def get_product_analysis(product_id):
    """
    Obtiene el análisis de un producto desde Firestore.
    Devuelve un diccionario o None si no existe.
    """
    doc_ref = _get_collection().document(str(product_id))
    doc = doc_ref.get()

    if not doc.exists:
        return None

    data = doc.to_dict()
    # Nos aseguramos de incluir el ID del documento
    data["product_id"] = product_id
    return data
