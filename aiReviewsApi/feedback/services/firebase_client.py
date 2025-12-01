from datetime import datetime
from django.conf import settings
from typing import Optional, List, Dict


COLLECTION_NAME = "product_analysis"
RUNS_COLLECTION = "analysis_runs"
HISTORY_COLLECTION = "product_analysis_history"
COMMENTS_COLLECTION = "product_comments"


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

def append_product_analysis_history(product_id, analysis_entry: dict):
    db = getattr(settings, "FIRESTORE_DB", None)
    if db is None:
        return
    doc = db.collection(HISTORY_COLLECTION).document(str(product_id))
    runs_col = doc.collection("runs")
    analysis_entry["created_at"] = datetime.utcnow().isoformat() + "Z"
    runs_col.add(analysis_entry)


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

def list_product_analyses():
    col = _get_collection()
    if col is None:
        return []
    results = []
    for doc in col.stream():
        d = doc.to_dict() or {}
        d["product_id"] = doc.id
        results.append(d)
    def _parse(ts):
        if not ts:
            return datetime.min
        try:
            return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        except Exception:
            return datetime.min
    results.sort(key=lambda x: _parse(x.get("last_analyzed_at")), reverse=True)
    return results
    
def query_product_analyses(
    product_name_contains: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> Dict[str, object]:
    items = list_product_analyses()
    q = (product_name_contains or "").strip().lower()
    if q:
        items = [it for it in items if q in str(it.get("product_name") or "").lower()]
    total = len(items)
    if page_size <= 0:
        page_size = 20
    if page <= 0:
        page = 1
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    return {
        "count": total,
        "page": page,
        "page_size": page_size,
        "results": items[start_idx:end_idx],
    }

def list_product_analysis_history(product_id):
    db = getattr(settings, "FIRESTORE_DB", None)
    if db is None:
        return []
    runs = db.collection(HISTORY_COLLECTION).document(str(product_id)).collection("runs")
    out = []
    for d in runs.stream():
        v = d.to_dict() or {}
        v["id"] = d.id
        out.append(v)
    def _parse(ts):
        if not ts:
            return datetime.min
        try:
            return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        except Exception:
            return datetime.min
    out.sort(key=lambda x: _parse(x.get("created_at")), reverse=True)
    return out

def save_product_comments(product_id: int, comments: list[dict]):
    db = getattr(settings, "FIRESTORE_DB", None)
    if db is None:
        return 0
    doc = db.collection(COMMENTS_COLLECTION).document(str(product_id))
    col = doc.collection("comments")
    count = 0
    for c in comments or []:
        item = dict(c or {})
        item["created_at"] = datetime.utcnow().isoformat() + "Z"
        col.add(item)
        count += 1
    return count

def list_product_comments(product_id: int):
    db = getattr(settings, "FIRESTORE_DB", None)
    if db is None:
        return []
    col = db.collection(COMMENTS_COLLECTION).document(str(product_id)).collection("comments")
    out = []
    for d in col.stream():
        v = d.to_dict() or {}
        v["id"] = d.id
        out.append(v)
    def _parse(ts):
        if not ts:
            return datetime.min
        try:
            return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        except Exception:
            return datetime.min
    out.sort(key=lambda x: _parse(x.get("created_at")), reverse=True)
    return out
    
def query_product_comments(
    product_id: int,
    q: Optional[str] = None,
    from_ts: Optional[str] = None,
    to_ts: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> Dict[str, object]:
    items = list_product_comments(product_id)
    q_norm = (q or "").strip().lower()
    def _parse2(ts):
        if not ts:
            return None
        try:
            return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        except Exception:
            return None
    start = _parse2(from_ts)
    end = _parse2(to_ts)
    filtered: List[Dict] = []
    for it in items:
        txt = (it.get("comment") or it.get("comentario") or "")
        when = _parse2(it.get("created_at"))
        if q_norm and q_norm not in str(txt).lower():
            continue
        if start and (not when or when < start):
            continue
        if end and (not when or when > end):
            continue
        filtered.append(it)
    total = len(filtered)
    if page_size <= 0:
        page_size = 20
    if page <= 0:
        page = 1
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    results = filtered[start_idx:end_idx]
    return {
        "count": total,
        "page": page,
        "page_size": page_size,
        "results": results,
    }

def save_analysis_run(run_data: dict):
    db = getattr(settings, "FIRESTORE_DB", None)
    if db is None:
        return None
    run_data = dict(run_data)
    run_data["created_at"] = datetime.utcnow().isoformat() + "Z"
    ref, _ = db.collection(RUNS_COLLECTION).add(run_data)
    return ref.id

def list_analysis_runs():
    db = getattr(settings, "FIRESTORE_DB", None)
    if db is None:
        return []
    results = []
    for d in db.collection(RUNS_COLLECTION).stream():
        v = d.to_dict() or {}
        v["id"] = d.id
        results.append(v)
    def _parse(ts):
        if not ts:
            return datetime.min
        try:
            return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        except Exception:
            return datetime.min
    results.sort(key=lambda x: _parse(x.get("created_at")), reverse=True)
    return results
