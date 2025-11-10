"""
Vista REST para analítica.
Expone un único endpoint que responde según query param `type`:
- type=top: ranking de productos por ingresos
- type=overview: panel general con totales
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status

from social.services.analytics_service import AnalyticsService


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        qtype = request.query_params.get('type')
        if qtype == 'top':
            try:
                # Parámetros opcionales: rango y límite
                range_days = int(request.query_params.get('range_days', 30))
                limit = int(request.query_params.get('limit', 10))
            except ValueError:
                return Response({'detail': 'Parámetros inválidos'}, status=status.HTTP_400_BAD_REQUEST)

            ranking = AnalyticsService.top_products(range_days=range_days, limit=limit)
            return Response({'type': 'top', 'data': ranking}, status=status.HTTP_200_OK)

        elif qtype == 'overview':
            data = AnalyticsService.overview()
            return Response({'type': 'overview', 'data': data}, status=status.HTTP_200_OK)

        return Response({'detail': 'type debe ser top u overview'}, status=status.HTTP_400_BAD_REQUEST)