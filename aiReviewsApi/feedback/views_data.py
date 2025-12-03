from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services.cloud_functions_client import (
    get_products,
    get_reviews,
    get_reviews_by_product
)


class ProductosView(APIView):
    def get(self, request):
        try:
            data = get_products()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


class ResenasView(APIView):
    def get(self, request):
        try:
            data = get_reviews()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


class ResenasPorProductoView(APIView):
    def get(self, request, product_id):
        try:
            data = get_reviews_by_product(product_id)
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "Producto no encontrado o sin reseñas"},
                status=status.HTTP_404_NOT_FOUND
            )
