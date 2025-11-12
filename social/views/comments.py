from rest_framework.views import APIView  # Vista base de DRF
from rest_framework.response import Response  # Respuesta JSON
from rest_framework import status  # Códigos de estado HTTP
from ..services.gemini_client import GeminiClient  # Cliente de Gemini
from ..services.firebase_client import FirestoreClient  # Cliente Firestore


class CommentsAnalyzeView(APIView):  # Analiza y persiste comentario e insight
    """Guarda un comentario, lo analiza con Gemini y persiste el insight."""  # Describe la vista

    def post(self, request):  # POST /v1/comments/analyze
        body = request.data or {}  # Body JSON
        product_id = body.get("product_id")  # Id de producto
        text = body.get("text")  # Texto del comentario
        rating = body.get("rating")  # Calificación opcional
        if not product_id or not text:  # Validación mínima
            return Response(  # Error de validación
                {"ok": False, "error": "Faltan 'product_id' o 'text'"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Inicializa clientes
        fc = FirestoreClient()  # Firestore
        gc = GeminiClient()  # Gemini
        # Persiste comentario
        comment_doc = {
            "product_id": product_id,
            "text": text,
            "rating": rating,
        }
        comment_id = fc.add_comment(comment_doc)  # Crea el documento en /comments
        # Analiza el texto
        analysis = gc.analyze_comment(text)  # Analiza sentimiento/toxicidad
        # Persiste insight con referencia al comentario
        insight_doc = {
            "product_id": product_id,
            "comment_id": comment_id,
            "analysis": analysis,
        }
        insight_id = fc.add_ai_insight(insight_doc)  # Crea documento en /ai_insights
        # Respuesta
        return Response(
            {
                "ok": True,
                "comment_id": comment_id,
                "insight_id": insight_id,
                "analysis": analysis,
            },
            status=status.HTTP_201_CREATED,
        )