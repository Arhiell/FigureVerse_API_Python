from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .services.analysis_service import (
    analyze_products_with_low_ratings,
    AnalysisError,
    analyze_general_opinion_for_products,
)
from .services.firebase_client import (
    get_product_analysis,
    list_product_analyses,
    list_analysis_runs,
    list_product_analysis_history,
    list_product_comments,
    save_product_comments,
    query_product_analyses,
    query_product_comments,
)
from .services.cloud_functions_client import get_reviews_by_product


@api_view(["POST"])
def analyze_low_rated_products(request):
    """
    POST /api/analisis/productos/malas-calificaciones/

    Body (opcional):
    {
        "rating_threshold": 3
    }
    """
    threshold = request.data.get("rating_threshold", 3)

    try:
        threshold = int(threshold)
    except (TypeError, ValueError):
        return Response(
            {"detail": "rating_threshold debe ser un número entero."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if threshold < 1 or threshold > 5:
        return Response(
            {"detail": "rating_threshold debe estar entre 1 y 5."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        result = analyze_products_with_low_ratings(threshold)
    except AnalysisError as exc:
        return Response(
            {"detail": str(exc)},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    return Response(result, status=status.HTTP_200_OK)


@api_view(["GET"])
def product_analysis_summary(request, product_id: int):
    """
    GET /api/analisis/productos/<product_id>/resumen/

    Devuelve el análisis guardado en Firebase para un producto.
    """
    data = get_product_analysis(product_id)

    if data is None:
        return Response(
            {"detail": "No hay análisis guardado para este producto."},
            status=status.HTTP_404_NOT_FOUND,
        )
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def product_analyses_list(request):
    page = int(request.GET.get("page", 1) or 1)
    page_size = int(request.GET.get("page_size", 20) or 20)
    q = request.GET.get("q") or request.GET.get("product_name")
    data = query_product_analyses(q, page=page, page_size=page_size)
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def analysis_runs_list(request):
    data = list_analysis_runs()
    return Response({"count": len(data), "results": data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def product_analysis_history_list(request, product_id: int):
    data = list_product_analysis_history(product_id)
    return Response({"count": len(data), "results": data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def product_comments_list(request, product_id: int):
    page = int(request.GET.get("page", 1) or 1)
    page_size = int(request.GET.get("page_size", 20) or 20)
    q = request.GET.get("q")
    from_ts = request.GET.get("from")
    to_ts = request.GET.get("to")
    data = query_product_comments(product_id, q=q, from_ts=from_ts, to_ts=to_ts, page=page, page_size=page_size)
    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
def sync_product_comments(request, product_id: int):
    try:
        reviews = get_reviews_by_product(product_id)
    except Exception as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
    items = reviews if isinstance(reviews, list) else (reviews.get("results") or [])
    saved = save_product_comments(product_id, items)
    return Response({"product_id": product_id, "saved": saved}, status=status.HTTP_200_OK)


@api_view(["GET"])
def product_opinion_summary(request, product_id: int):
    data = get_product_analysis(product_id)
    if not data or not data.get("general_opinion"):
        return Response({"detail": "No hay opinión general guardada para este producto."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"product_id": product_id, "product_name": data.get("product_name"), "general_opinion": data.get("general_opinion")}, status=status.HTTP_200_OK)


@api_view(["POST"])
def sync_product_opinions(request):
    try:
        result = analyze_general_opinion_for_products()
    except AnalysisError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
    return Response(result, status=status.HTTP_200_OK)
