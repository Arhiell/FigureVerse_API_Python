from social.models.rating import Rating
from django.db.models import Avg, Count


class RatingService:
    """
    Servicio encargado de manejar la lógica de negocio relacionada con las calificaciones.
    """

    @staticmethod
    def create_rating(data):
        """
        Crea una nueva calificación usando los datos proporcionados.
        """
        return Rating.objects.create(**data)

    @staticmethod
    def get_summary(product_id):
        """
        Calcula el promedio y la cantidad de calificaciones de un producto.
        Se utiliza agregación de Django ORM.
        """
        summary = Rating.objects.filter(product_id=product_id).aggregate(
            promedio=Avg('score'),
            cantidad=Count('score')
        )
        return summary