from social.models.comment import Comment


class CommentService:
    """
    Servicio encargado de la lógica del negocio:
    crear, listar y gestionar los comentarios.
    No interactúa con HTTP directamente, solo maneja operaciones internas.
    """

    @staticmethod
    def create_comment(data):
        """
        Crea un nuevo comentario en la base de datos usando los datos recibidos.
        """
        return Comment.objects.create(**data)

    @staticmethod
    def list_comments(product_id):
        """
        Devuelve los comentarios aprobados asociados a un producto específico.
        """
        return Comment.objects.filter(product_id=product_id, status="aprobado")