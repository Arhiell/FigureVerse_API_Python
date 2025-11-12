from django.db import models  # Importa utilidades de modelos de Django


class Event(models.Model):  # Modelo opcional para usos locales
    """Modelo opcional para futuros usos locales.
    No se utiliza en el test inicial; Firestore es la fuente.
    """  # Describe el propósito del modelo
    external_id = models.CharField(max_length=128, unique=True)  # ID externo (doc.id en Firestore)
    type = models.CharField(max_length=64)  # Tipo de evento
    timestamp = models.DateTimeField()  # Marca temporal del evento

    class Meta:  # Metadatos del modelo
        ordering = ["-timestamp"]  # Orden por timestamp descendente


class ProductStats(models.Model):  # Métricas agregadas por producto
    """Almacena métricas agregadas de cada producto."""  # Documenta el modelo

    product_id = models.CharField(max_length=50, unique=True)  # Identificador del producto (único)
    avg_rating = models.FloatField(default=0)  # Promedio de calificaciones
    ratings_count = models.IntegerField(default=0)  # Cantidad de calificaciones
    comments_count = models.IntegerField(default=0)  # Cantidad de comentarios
    reputation_index = models.FloatField(default=0)  # Índice de reputación (IA)
    sales_total = models.FloatField(default=0)  # Total de ventas acumuladas
    last_event = models.CharField(max_length=100, blank=True)  # Último evento que impactó
    updated_at = models.DateTimeField(auto_now=True)  # Última actualización

    def __str__(self):  # Representación legible
        return f"ProductStats(product_id={self.product_id})"  # Muestra el product_id


class SyncCursor(models.Model):  # Control de sincronización de eventos
    """Controla el punto de sincronización (último evento procesado)."""  # Documenta el modelo

    last_timestamp = models.DateTimeField(null=True, blank=True)  # Último timestamp procesado
    last_event_id = models.CharField(max_length=100, blank=True)  # Id/tipo del último evento

    def __str__(self):  # Representación legible
        return f"SyncCursor(last_timestamp={self.last_timestamp}, last_event_id={self.last_event_id})"  # Muestra últimos valores