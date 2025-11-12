from rest_framework.views import APIView  # Vista base de DRF
from rest_framework.response import Response  # Respuesta HTTP JSON
from rest_framework import status  # Códigos HTTP
from ..services.analytics_service import (  # Importa funciones del servicio
    get_overview,
    get_top_products,
    recalculate_and_publish,
)  # Incluye recálculo


class OverviewView(APIView):  # Endpoint para resumen general
    """Devuelve métricas generales (ventas y conteo) junto al top."""  # Describe la vista

    def get(self, request):  # Maneja solicitudes GET
        data = get_overview()  # Obtiene datos del servicio
        return Response(data)  # Retorna JSON con el resumen


class TopProductsView(APIView):  # Endpoint para top de productos
    """Devuelve el top de productos por reputación."""  # Describe la vista

    def get(self, request):  # Maneja solicitudes GET
        items = get_top_products()  # Obtiene el top (por defecto 10)
        return Response({"items": items})  # Retorna JSON con la lista


class AnalyticsRecalculateView(APIView):  # Recalcula y publica métricas en Firestore
    """Recalcula métricas desde eventos y publica resultados en Firestore."""  # Describe la vista

    def post(self, request):  # Solo POST
        result = recalculate_and_publish()  # Ejecuta recálculo
        return Response(result, status=status.HTTP_200_OK)  # Devuelve resumen de la operación