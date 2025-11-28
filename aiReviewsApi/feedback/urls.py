from django.urls import path
from .views_data import (
    ProductosView,
    ResenasView,
    ResenasPorProductoView
)

urlpatterns = [
    path("productos/", ProductosView.as_view()),
    path("resenas/", ResenasView.as_view()),
    path("resenas/producto/<int:product_id>/", ResenasPorProductoView.as_view()),
]
