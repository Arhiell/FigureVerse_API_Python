from typing import List, Dict, Any
from django.conf import settings
import google.generativeai as genai


class GeminiError(Exception):
    """Error genérico al llamar a Gemini."""
    pass


# Configuramos Gemini con la API key definida en settings
genai.configure(api_key=settings.GEMINI_API_KEY)

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
Analiza las reseñas de un producto y genera un resumen en español.

Información del producto:
- ID: {product_id}
- Nombre: {product_name}
- Descripción: {product_desc}

Estadísticas:
- Calificación promedio: {avg_rating:.2f}
- Total de reseñas: {total_reviews}
- Umbral de mala calificación: {rating_threshold} (se consideran reseñas malas si la calificación es <= {rating_threshold})

Reseñas con calificación baja (una por línea):
{reviews_text}

TAREA:
1. Resume los principales problemas o quejas que tienen los clientes sobre este producto.
2. Si hay aspectos positivos destacables, menciónalos de forma breve.
3. Usa un lenguaje claro, conciso y enfocado en patrones (no menciones reseñas individuales).
4. Máximo 2 párrafos.
"""

    try:
        model = genai.GenerativeModel(_MODEL_NAME)
        response = model.generate_content(prompt)
        # En la mayoría de los casos, la respuesta de texto está en response.text
        summary = response.text
        return summary.strip()
    except Exception as exc:
        raise GeminiError(f"Error al generar resumen con Gemini: {exc}")
