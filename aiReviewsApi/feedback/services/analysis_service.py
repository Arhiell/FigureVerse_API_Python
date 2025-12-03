from typing import Dict, Any
from statistics import mean

from .cloud_functions_client import (
    get_products,
    get_all_reviews,
    CloudFunctionsError,
)
from .firebase_client import save_product_analysis, append_product_analysis_history, save_analysis_run
from .gemini_client import summarize_low_rating_reviews, summarize_general_opinion, GeminiError


class AnalysisError(Exception):
    """Error genérico en el proceso de análisis."""
    pass


def analyze_products_with_low_ratings(rating_threshold: int) -> Dict[str, Any]:
    """
    Analiza productos que tengan reseñas con calificación <= rating_threshold.
    Usa Cloud Functions para leer datos, Gemini para resumir y Firebase para guardar.

    Devuelve un dict con estadísticas globales:
    {
        "rating_threshold": ...,
        "analyzed_products": ...,
        "total_products": ...,
    }
    """
    try:
        products = get_products()
        all_reviews = get_all_reviews()
    except CloudFunctionsError as exc:
        # Reempaquetamos el error con un tipo propio
        raise AnalysisError(f"Error al leer datos desde Cloud Functions: {exc}")

    # Indexamos reseñas por producto
    reviews_by_product = {}
    for r in all_reviews:
        product_id = r.get("product_id") or r.get("id_producto")
        if product_id is None:
            continue

        reviews_by_product.setdefault(product_id, []).append(r)

    analyzed_count = 0
    analyzed_names = []
    summaries = []

    # Suponemos que products es una lista de diccionarios con campo 'id' o 'id_producto'
    for p in products:
        product_id = p.get("id") or p.get("id_producto")
        if product_id is None:
            continue

        product_reviews = reviews_by_product.get(product_id, [])

        if not product_reviews:
            # Si el producto no tiene reseñas, no lo analizamos
            continue

        # Obtenemos el rating de cada reseña
        ratings = []
        for r in product_reviews:
            rating_value = r.get("rating") or r.get("calificacion")
            try:
                # Intentamos convertir a float/int
                ratings.append(float(rating_value))
            except (TypeError, ValueError):
                continue

        if not ratings:
            continue

        avg_rating = mean(ratings)
        total_reviews = len(ratings)

        # Reseñas con mala calificación (<= threshold)
        low_rating_reviews = [
            r for r, rv in zip(product_reviews, ratings)
            if rv <= rating_threshold
        ]

        if not low_rating_reviews:
            # Si no hay reseñas malas, no tiene sentido generar resumen
            continue

        # Llamamos a Gemini para generar el resumen de reseñas malas
        try:
            summary = summarize_low_rating_reviews(
                product=p,
                low_rating_reviews=low_rating_reviews,
                rating_threshold=rating_threshold,
                avg_rating=avg_rating,
                total_reviews=total_reviews,
            )
        except GeminiError as exc:
            # Podríamos registrar el error y continuar con otros productos
            # Por ahora, lo propagamos
            raise AnalysisError(f"Error al analizar producto {product_id}: {exc}")

        analysis_data = {
            "product_name": p.get("name") or p.get("nombre"),
            "rating_threshold": rating_threshold,
            "avg_rating": avg_rating,
            "total_reviews": total_reviews,
            "low_rating_reviews_count": len(low_rating_reviews),
            "summary": summary,
        }

        save_product_analysis(product_id, analysis_data)
        analyzed_count += 1
        product_name = analysis_data["product_name"]
        if product_name:
            analyzed_names.append(product_name)
        summaries.append({
            "product_id": product_id,
            "product_name": product_name,
            "summary": summary,
        })
        append_product_analysis_history(product_id, analysis_data)

    run = {
        "rating_threshold": rating_threshold,
        "analyzed_products": analyzed_names,
        "analyzed_count": analyzed_count,
        "total_products": len(products),
        "summaries": summaries,
    }
    try:
        save_analysis_run(run)
    except Exception:
        pass
    result = run

    return result


def analyze_general_opinion_for_products() -> Dict[str, Any]:
    try:
        products = get_products()
        all_reviews = get_all_reviews()
    except CloudFunctionsError as exc:
        raise AnalysisError(f"Error al leer datos desde Cloud Functions: {exc}")

    reviews_by_product = {}
    for r in all_reviews:
        product_id = r.get("product_id") or r.get("id_producto")
        if product_id is None:
            continue
        reviews_by_product.setdefault(product_id, []).append(r)

    analyzed_count = 0
    analyzed_names = []
    summaries = []

    for p in products:
        product_id = p.get("id") or p.get("id_producto")
        if product_id is None:
            continue
        product_reviews = reviews_by_product.get(product_id, [])
        if not product_reviews:
            continue

        ratings = []
        for r in product_reviews:
            rating_value = r.get("rating") or r.get("calificacion")
            try:
                ratings.append(float(rating_value))
            except (TypeError, ValueError):
                continue
        avg_rating = mean(ratings) if ratings else 0.0
        total_reviews = len(product_reviews)

        try:
            summary = summarize_general_opinion(product=p, reviews=product_reviews)
        except GeminiError as exc:
            raise AnalysisError(f"Error al analizar producto {product_id}: {exc}")

        analysis_data = {
            "product_name": p.get("name") or p.get("nombre"),
            "avg_rating": avg_rating,
            "total_reviews": total_reviews,
            "general_opinion": summary,
        }

        save_product_analysis(product_id, analysis_data)
        analyzed_count += 1
        product_name = analysis_data["product_name"]
        if product_name:
            analyzed_names.append(product_name)
        summaries.append({
            "product_id": product_id,
            "product_name": product_name,
            "general_opinion": summary,
        })
        append_product_analysis_history(product_id, analysis_data)

    run = {
        "analyzed_products": analyzed_names,
        "analyzed_count": analyzed_count,
        "total_products": len(products),
        "general_summaries": summaries,
    }
    try:
        save_analysis_run(run)
    except Exception:
        pass
    return run
