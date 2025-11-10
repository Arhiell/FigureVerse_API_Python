from django.db import models


class Rating(models.Model):
    """
    Modelo que representa una calificación otorgada por un usuario a un producto.
    La puntuación debe estar en el rango de 1 a 5.
    """

    product_id = models.IntegerField()
    # Identificador del producto proveniente de la API principal en Node

    user_id = models.CharField(max_length=255)
    # ID único del usuario autenticado que hizo la calificación

    score = models.IntegerField()
    # La puntuación asignada por el usuario, debe ser un valor entre 1 y 5

    created_at = models.DateTimeField(auto_now_add=True)
    # Fecha y hora automática de cuando se registra la calificación

    def __str__(self):
        """
        Representación legible del objeto para depuración y panel de administración.
        """
        return f"Rating(product={self.product_id}, user={self.user_id}, score={self.score})"