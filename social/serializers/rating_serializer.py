from rest_framework import serializers
from social.models.rating import Rating


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializador que convierte objetos Rating en JSON y valida los datos recibidos.
    """

    class Meta:
        model = Rating
        fields = '__all__'

    def validate_score(self, value):
        """
        Valida que la puntuación esté dentro del rango permitido (1 a 5).
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("La calificación debe estar entre 1 y 5.")
        return value