from django.urls import path
from . import views_data
from . import views_analysis

urlpatterns = [
    # --- Endpoints de datos crudos (Cloud Functions) ---

    # GET /api/productos/
    path("productos/", views_data.productos_list, name="productos-list"),

    # GET /api/resenas/
    path("resenas/", views_data.resenas_list, name="resenas-list"),

    # GET /api/resenas/producto/<id>/
    path(
        "resenas/producto/<int:product_id>/",
        views_data.resenas_by_product,
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
