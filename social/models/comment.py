from django.db import models


class Comment(models.Model):
    """
    Modelo que representa un comentario realizado por un usuario sobre un producto.
    Este modelo será utilizado por Django ORM para crear la tabla correspondiente.
    """

    product_id = models.IntegerField()  # ID del producto proveniente de la API Node
    user_id = models.CharField(max_length=255)  # ID del usuario autenticado
    content = models.TextField()  # Texto del comentario
    status = models.CharField(max_length=20, default="pendiente")
    # El estado define si el comentario está aprobado, rechazado o pendiente
    created_at = models.DateTimeField(auto_now_add=True)
    # Se asigna la fecha y hora automáticamente cuando el comentario es creado

    def __str__(self):
        # Representación legible del comentario, útil en admin/django shell
        return f"Comment(user={self.user_id}, product={self.product_id}, status={self.status})"