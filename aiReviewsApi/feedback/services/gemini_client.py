from typing import List, Dict, Any
from django.conf import settings
import google.generativeai as genai


class GeminiError(Exception):
    """Error genérico al llamar a Gemini."""
    pass


_API_KEY = settings.GEMINI_API_KEY
try:
    genai.configure(api_key=_API_KEY)
except Exception:
    pass

# Podés cambiar el modelo si querés
_MODEL_NAME = "gemini-1.5-flash"


def summarize_low_rating_reviews(
    product: Dict[str, Any],
    low_rating_reviews: List[Dict[str, Any]],
    rating_threshold: int,
    avg_rating: float,
    total_reviews: int,
) -> str:
    """
    Llama a Gemini para generar un resumen de las reseñas con mala calificación
    de un producto.

    - product: dict con al menos 'id' y 'name'/'nombre'
    - low_rating_reviews: lista de reseñas de ese producto con calificación <= threshold
    - rating_threshold: umbral considerado como "mala" calificación
    - avg_rating: promedio de calificaciones del producto
    - total_reviews: cantidad total de reseñas del producto
    """

    if not low_rating_reviews:
        return "No se encontraron reseñas con calificación baja para este producto."

    # Extraemos algunos campos del producto con nombres genéricos
    product_id = product.get("id") or product.get("id_producto") or "desconocido"
    product_name = product.get("name") or product.get("nombre") or "Producto sin nombre"
    product_desc = product.get("description") or product.get("descripcion") or ""

    # Limitamos la cantidad de reseñas para no mandar textos enormes
    max_reviews = 50
    reviews_sample = low_rating_reviews[:max_reviews]

    # Armamos el texto de reseñas
    reviews_text_lines = []
    for idx, r in enumerate(reviews_sample, start=1):
        rating = r.get("rating") or r.get("calificacion") or "?"
        comment = r.get("comment") or r.get("comentario") or ""
        reviews_text_lines.append(f"{idx}. Calificación: {rating} - Comentario: {comment}")

    reviews_text = "\n".join(reviews_text_lines)

    prompt = f"""
Analiza reseñas de un producto y devuelve UNA SOLA FRASE clara en español.

Contexto del producto:
- ID: {product_id}
- Nombre: {product_name}
- Descripción: {product_desc}

Estadísticas:
- Calificación promedio: {avg_rating:.2f}
- Total de reseñas: {total_reviews}
- Umbral de mala calificación: {rating_threshold}

Muestra de reseñas malas (una por línea):
{reviews_text}

Instrucciones:
- Redacta una única oración concisa (<= 25 palabras) que resuma patrones de quejas y, si corresponde, un aspecto positivo.
- No enumeres ni cites reseñas específicas.
- No generes más de una oración.
"""

    if not _API_KEY:
        positives = []
        negatives = []
        for r in reviews_sample:
            txt = (r.get("comment") or r.get("comentario") or "").lower()
            if any(k in txt for k in ["bueno", "excelente", "positivo", "recomendado", "cumple"]):
                positives.append(txt)
            if any(k in txt for k in ["malo", "defecto", "fallo", "problema", "no funciona", "devuelve"]):
                negatives.append(txt)
        neg_phrase = "quejas recurrentes" if negatives else "sin patrón claro de quejas"
        pos_phrase = "algunos aspectos positivos" if positives else "pocos aspectos positivos"
        return f"{product_name}: {neg_phrase} y {pos_phrase}."

    try:
        model = genai.GenerativeModel(_MODEL_NAME)
        response = model.generate_content(prompt)
        summary = response.text
        return summary.strip()
    except Exception as exc:
        positives = []
        negatives = []
        for r in reviews_sample:
            txt = (r.get("comment") or r.get("comentario") or "").lower()
            if any(k in txt for k in ["bueno", "excelente", "positivo", "recomendado", "cumple"]):
                positives.append(txt)
            if any(k in txt for k in ["malo", "defecto", "fallo", "problema", "no funciona", "devuelve"]):
                negatives.append(txt)
        neg_phrase = "quejas recurrentes" if negatives else "sin patrón claro de quejas"
        pos_phrase = "algunos aspectos positivos" if positives else "pocos aspectos positivos"
        return f"{product_name}: {neg_phrase} y {pos_phrase}."


def summarize_general_opinion(product: Dict[str, Any], reviews: List[Dict[str, Any]]) -> str:
    product_id = product.get("id") or product.get("id_producto") or "desconocido"
    product_name = product.get("name") or product.get("nombre") or "Producto sin nombre"
    product_desc = product.get("description") or product.get("descripcion") or ""

    max_reviews = 100
    sample = reviews[:max_reviews]

    lines = []
    for idx, r in enumerate(sample, start=1):
        rating = r.get("rating") or r.get("calificacion") or "?"
        comment = r.get("comment") or r.get("comentario") or ""
        lines.append(f"{idx}. {rating}: {comment}")
    reviews_text = "\n".join(lines)

    prompt = (
        "Analiza reseñas de un producto y devuelve una sola frase en español con la opinión general, "
        "equilibrando aspectos positivos y negativos, sin enumerar reseñas ni citar textualmente.\n\n"
        f"ID: {product_id}\nNombre: {product_name}\nDescripción: {product_desc}\n\n"
        f"Muestra de reseñas:\n{reviews_text}\n\n"
        "Una única oración concisa (≤ 25 palabras)."
    )

    if not _API_KEY:
        positives = []
        negatives = []
        for r in sample:
            txt = (r.get("comment") or r.get("comentario") or "").lower()
            if any(k in txt for k in ["bueno", "excelente", "positivo", "recomendado", "cumple"]):
                positives.append(txt)
            if any(k in txt for k in ["malo", "defecto", "fallo", "problema", "no funciona", "devuelve"]):
                negatives.append(txt)
        neg_phrase = "quejas recurrentes" if negatives else "sin patrón claro de quejas"
        pos_phrase = "algunos aspectos positivos" if positives else "pocos aspectos positivos"
        return f"{product_name}: {neg_phrase} y {pos_phrase}."

    try:
        model = genai.GenerativeModel(_MODEL_NAME)
        response = model.generate_content(prompt)
        return (response.text or "").strip()
    except Exception:
        positives = []
        negatives = []
        for r in sample:
            txt = (r.get("comment") or r.get("comentario") or "").lower()
            if any(k in txt for k in ["bueno", "excelente", "positivo", "recomendado", "cumple"]):
                positives.append(txt)
            if any(k in txt for k in ["malo", "defecto", "fallo", "problema", "no funciona", "devuelve"]):
                negatives.append(txt)
        neg_phrase = "quejas recurrentes" if negatives else "sin patrón claro de quejas"
        pos_phrase = "algunos aspectos positivos" if positives else "pocos aspectos positivos"
        return f"{product_name}: {neg_phrase} y {pos_phrase}."
