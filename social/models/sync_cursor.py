from django.db import models  # Importa utilidades de modelos de Django


class SyncCursor(models.Model):  # Define el modelo para control de sincronización
    """Controla el punto de sincronización (último evento procesado)."""  # Describe el propósito del modelo

    last_timestamp = models.DateTimeField(null=True, blank=True)  # Última marca temporal procesada
    last_event_id = models.CharField(max_length=100, blank=True)  # ID/Tipo del último evento procesado

    def __str__(self):  # Representación legible del registro
        return f"SyncCursor(last_timestamp={self.last_timestamp}, last_event_id={self.last_event_id})"  # Muestra últimos valores