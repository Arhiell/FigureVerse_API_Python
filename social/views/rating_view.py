from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from social.serializers.rating_serializer import RatingSerializer
from social.services.rating_service import RatingService


class RatingView(APIView):
    """
    Vista encargada de manejar solicitudes HTTP relacionadas con calificaciones.
    Requiere autenticación válida mediante JWT.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        """
        Crea una nueva calificación para un producto específico.
        El ID del producto se obtiene desde la URL.
        """
        data = {
            "product_id": id,
            "user_id": request.user.id,
            "score": request.data.get("score"),
        }

        serializer = RatingSerializer(data=data)

        # Validación de la estructura de datos
        serializer.is_valid(raise_exception=True)

        rating = RatingService.create_rating(serializer.validated_data)

        return Response(RatingSerializer(rating).data)

    def get(self, request, id):
        """
        Devuelve el resumen de calificaciones de un producto.
        Retorna promedio y cantidad de ratings.
        """
        summary = RatingService.get_summary(id)

        return Response({
            "product_id": id,
            "promedio": summary["promedio"],
            "cantidad": summary["cantidad"],
        })