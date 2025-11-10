from rest_framework import serializers
from social.models.comment import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializador que transforma el modelo Comment en datos JSON.
    También valida la estructura antes de crear o actualizar un registro.
    """

    class Meta:
        model = Comment
        fields = '__all__'