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
    path(
        "analisis/productos/resumenes/",
        views_analysis.product_analyses_list,
        name="product-analyses-list",
    ),
    path(
        "analisis/runs/",
        views_analysis.analysis_runs_list,
        name="analysis-runs-list",
    ),
    path(
        "analisis/productos/<int:product_id>/historial/",
        views_analysis.product_analysis_history_list,
        name="product-analysis-history",
    ),
    path(
        "comentarios/producto/<int:product_id>/",
        views_analysis.product_comments_list,
        name="product-comments-list",
    ),
    path(
        "comentarios/producto/<int:product_id>/sync/",
        views_analysis.sync_product_comments,
        name="product-comments-sync",
    ),
]
