from django.urls import path
from social.views.rating_view import RatingView


urlpatterns = [
    # Crea la calificación y obtiene el resumen del producto
    path('<int:id>/ratings', RatingView.as_view()),
]