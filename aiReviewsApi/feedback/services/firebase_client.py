from datetime import datetime
from django.conf import settings


COLLECTION_NAME = "product_analysis"


def _get_collection():
    """
    Devuelve la referencia a la colección de análisis en Firestore.
    Si FIRESTORE_DB no está configurado, devuelve None para no romper en desarrollo.
    """
    db = getattr(settings, "FIRESTORE_DB", None)
    if db is None:
        return None
    return db.collection(COLLECTION_NAME)


def save_product_analysis(product_id, analysis_data: dict):
    """
    Guarda (o actualiza) el análisis de un producto en Firestore.

    - product_id: ID del producto (int o str)
    - analysis_data: diccionario con los campos del análisis
    """
    col = _get_collection()
    if col is None:
        # Entorno sin Firebase configurado: no guardamos pero no rompemos
        return
    doc_ref = col.document(str(product_id))

    # Siempre agregamos/actualizamos la fecha de último análisis
    analysis_data["last_analyzed_at"] = datetime.utcnow().isoformat() + "Z"

    # Usamos merge=True para no sobreescribir campos que no están en analysis_data
    doc_ref.set(analysis_data, merge=True)


def get_product_analysis(product_id):
    """
    Obtiene el análisis de un producto desde Firestore.
    Devuelve un diccionario o None si no existe.
    """
    col = _get_collection()
    if col is None:
        # Entorno sin Firebase: comportarnos como si no existiera análisis
        return None
    doc_ref = col.document(str(product_id))
    doc = doc_ref.get()

    if not doc.exists:
        return None

    data = doc.to_dict()
    # Nos aseguramos de incluir el ID del documento
    data["product_id"] = product_id
    return data
