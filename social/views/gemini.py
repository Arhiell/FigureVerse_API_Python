from rest_framework.views import APIView  # Vista base DRF
from rest_framework.response import Response  # Respuesta JSON
from rest_framework import status  # Códigos de estado HTTP
from ..services.gemini_client import GeminiClient  # Cliente de Gemini


class CommentsAnalysisView(APIView):  # Analiza comentarios para un producto
    """Analiza el texto de un comentario usando Gemini."""  # Describe la vista

    def post(self, request, product_id: str):  # POST con texto en el body
        text = request.data.get("text")  # Extrae el texto a analizar
        if not text:  # Si falta el texto
            return Response(  # Responde error
                {"ok": False, "error": "Falta 'text' en el body"},  # Mensaje
                status=status.HTTP_400_BAD_REQUEST,  # Código 400
            )
        gc = GeminiClient()  # Inicializa el cliente de Gemini
        result = gc.analyze_comment(text)  # Analiza el comentario
        return Response({"ok": True, "product_id": product_id, "analysis": result})  # Devuelve análisis

    def get(self, request, product_id: str):  # GET con texto como query param
        text = request.query_params.get("text")  # Lee ?text=...
        if not text:  # Si falta
            return Response(  # Responde mensaje de ayuda
                {
                    "ok": False,
                    "error": "Provee ?text= para analizar o usa POST con body JSON",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        gc = GeminiClient()  # Inicializa el cliente
        result = gc.analyze_comment(text)  # Analiza
        return Response({"ok": True, "product_id": product_id, "analysis": result})  # Devuelve resultado


class AdminQuestionsView(APIView):  # Preguntas libres del admin a la IA
    """Permite hacer preguntas libres al modelo Gemini."""  # Describe la vista

    def post(self, request):  # POST con campo 'question'
        question = request.data.get("question")  # Extrae pregunta
        if not question:  # Si falta
            return Response(  # Devuelve error
                {"ok": False, "error": "Falta 'question' en el body"},  # Mensaje
                status=status.HTTP_400_BAD_REQUEST,  # Código 400
            )
        gc = GeminiClient()  # Inicializa cliente
        result = gc.ask_question(question)  # Consulta al modelo
        return Response({"ok": True, "answer": result.get("answer"), "raw": result.get("raw")})  # Respuesta