from typing import List, Dict  # Tipos para listas y diccionarios
from .firebase_client import FirestoreClient  # Cliente Firestore


def get_top_products(limit: int = 10) -> List[Dict]:  # Obtiene los productos con mejor reputación
    """Devuelve los productos con mejor reputación desde Firestore."""  # Documenta la función
    fc = FirestoreClient()  # Inicializa cliente
    return fc.get_top_product_stats(limit=limit)  # Delegamos lectura al cliente Firestore


def get_overview() -> Dict:  # Resumen general del negocio
    """Lee overview desde Firestore y añade top de productos."""  # Documenta la función
    fc = FirestoreClient()  # Cliente Firestore
    overview = fc.get_analytics_overview()  # Lee documento overview
    overview = overview or {"total_ventas": 0, "total_productos": 0}  # Valores por defecto
    overview["top"] = get_top_products(5)  # Adjunta top 5
    return overview  # Devuelve estructura


def recalculate_and_publish() -> Dict:  # Recalcula métricas y las publica en Firestore
    """Recalcula métricas desde eventos y publica en analytics/product_stats."""  # Documenta función
    fc = FirestoreClient()  # Cliente Firestore
    overview, product_stats_docs = fc.aggregate_from_events()  # Calcula métricas
    # Publica overview
    fc.set_analytics_overview(overview)  # Guarda resumen
    # Publica cada product_stat
    for pid, doc in product_stats_docs.items():  # Itera resultados por producto
        fc.upsert_product_stat(pid, doc)  # Upsert
    # Devuelve resumen de la operación
    return {
        "updated_products": len(product_stats_docs),  # Cantidad de productos actualizados
        "overview": overview,  # Datos del overview guardado
    }