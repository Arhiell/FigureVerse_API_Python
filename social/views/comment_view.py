from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from social.serializers.comment_serializer import CommentSerializer
from social.services.comment_service import CommentService
from social.services import node_client


class CommentView(APIView):
    """
    Vista HTTP que maneja las solicitudes relacionadas con los comentarios.
    Requiere que el usuario esté autenticado mediante JWT.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """
        Lista los comentarios aprobados para el producto indicado.
        """
        comments = CommentService.list_comments(product_id=id)
        return Response(CommentSerializer(comments, many=True).data)

    def post(self, request, id):
        """
        Crea un nuevo comentario para el producto indicado.
        El ID del producto llega desde la URL.
        """
        # Validamos que exista contenido en el cuerpo de la petición.
        content = request.data.get("content")
        if not content or not str(content).strip():
            return Response({"detail": "El campo 'content' es requerido"}, status=400)

        # Validamos contra la API de Node que el producto exista.
        # Usamos el token propagado por la autenticación para llamadas autorizadas.
        token = getattr(request, "auth", None)
        try:
            node_client.get_product(product_id=id, token=token)
        except Exception as exc:
            # Intentamos diferenciar 404 de otros errores para responder adecuadamente.
            status_code = getattr(getattr(exc, "response", None), "status_code", 502)
            message = "Producto no encontrado" if status_code == 404 else "Error al validar producto en Node"
            return Response({"detail": message}, status=status_code)

        data = {
            "product_id": id,
            "user_id": request.user.id,
            # Se obtiene el usuario autenticado desde el JWT validado
            "content": content,
            # Se recibe el texto del comentario desde el cuerpo de la petición
        }

        comment = CommentService.create_comment(data)
        # Se invoca al servicio encargado de crear el comentario

        return Response(CommentSerializer(comment).data)
        # Se devuelve el comentario nuevo en formato JSON