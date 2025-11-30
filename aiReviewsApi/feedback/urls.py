from django.urls import path
from .views_data import (
    ProductosView,
    ResenasView,
    ResenasPorProductoView,
)
from . import views_analysis

urlpatterns = [
    # --- Endpoints de datos crudos (Cloud Functions) ---

    # GET /api/productos/
    path("productos/", ProductosView.as_view(), name="productos-list"),

    # GET /api/resenas/
    path("resenas/", ResenasView.as_view(), name="resenas-list"),

    # GET /api/resenas/producto/<id>/
    path(
        "resenas/producto/<int:product_id>/",
        ResenasPorProductoView.as_view(),
        name="resenas-by-product",
    ),

    # --- Endpoints de análisis (Gemini + Firebase) ---

    # POST /api/analisis/productos/malas-calificaciones/
    path(
        "analisis/productos/malas-calificaciones/",
        views_analysis.analyze_low_rated_products,
        name="analisis-low-rated-products",
    ),

    # GET /api/analisis/productos/<id>/resumen/
    path(
        "analisis/productos/<int:product_id>/resumen/",
        views_analysis.product_analysis_summary,
        name="product-analysis-summary",
    ),
]
