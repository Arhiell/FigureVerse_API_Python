from django.urls import path
from social.views.comment_view import CommentView

urlpatterns = [
    # Esta ruta permite publicar un comentario sobre un producto específico
    path('<int:id>/comments', CommentView.as_view()),
]