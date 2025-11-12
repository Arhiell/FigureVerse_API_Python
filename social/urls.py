from django.urls import path  # Constructor de rutas
from .views.firebase_test import FirebaseTestView  # Vista de prueba Firebase
from .views.analytics import (  # Vistas para endpoints de análisis
    OverviewView,
    TopProductsView,
    AnalyticsRecalculateView,
)  # Importa las vistas nuevas
from .views.gemini import (  # Vistas para endpoints de IA
    CommentsAnalysisView,
    AdminQuestionsView,
)  # Importa vistas de Gemini
from .views.comments import CommentsAnalyzeView  # Endpoint POST /v1/comments/analyze


urlpatterns = [  # Lista de rutas públicas bajo /v1/
    path("firebase/test", FirebaseTestView.as_view()),  # Prueba de Firestore
    path("analytics/overview", OverviewView.as_view()),  # Resumen de negocio
    path("analytics/top-products", TopProductsView.as_view()),  # Top productos
    path("analytics/recalculate", AnalyticsRecalculateView.as_view()),  # Recalcular métricas
    path("comments/<str:product_id>/analysis", CommentsAnalysisView.as_view()),  # Analiza comentarios
    path("admin/questions", AdminQuestionsView.as_view()),  # Preguntas del admin a IA
    path("comments/analyze", CommentsAnalyzeView.as_view()),  # Analiza y persiste comentario
]