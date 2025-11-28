from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .services.analysis_service import (
    analyze_products_with_low_ratings,
    AnalysisError,
)
from .services.firebase_client import get_product_analysis


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
