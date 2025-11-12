from django.db import models  # Importa utilidades de modelos de Django


class ProductStats(models.Model):  # Define el modelo para métricas por producto
    """Almacena métricas agregadas de cada producto."""  # Describe el propósito del modelo

    product_id = models.CharField(max_length=50, unique=True)  # Identificador del producto (único)
    avg_rating = models.FloatField(default=0)  # Promedio de calificaciones
    ratings_count = models.IntegerField(default=0)  # Cantidad de calificaciones registradas
    comments_count = models.IntegerField(default=0)  # Cantidad de comentarios registrados
    reputation_index = models.FloatField(default=0)  # Índice de reputación calculado por IA
    sales_total = models.FloatField(default=0)  # Total de ventas acumuladas
    last_event = models.CharField(max_length=100, blank=True)  # Último evento que afectó estas métricas
    updated_at = models.DateTimeField(auto_now=True)  # Marca de tiempo de última actualización

    def __str__(self):  # Representación legible del registro
        return f"ProductStats(product_id={self.product_id})"  # Devuelve el identificador del producto