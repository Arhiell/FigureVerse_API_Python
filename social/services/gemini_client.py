try:  # Intenta importar el SDK de Gemini
    import google.generativeai as genai  # Cliente de Gemini
except Exception:  # Si no está instalado o falla
    genai = None  # Deja referencia nula para manejo posterior

from django.conf import settings  # Configuración de Django


class GeminiClient:  # Cliente para interactuar con Gemini
    """Cliente simple para análisis de texto con Gemini."""  # Describe la clase

    def __init__(self):  # Inicializa el cliente
        # Verifica que el SDK esté disponible
        if genai is None:  # Si falta la librería
            raise RuntimeError(
                "google.generativeai no está instalado. Instala 'google-generativeai'."
            )  # Informa al desarrollador
        # Configura el API key desde settings
        api_key = getattr(settings, "GEMINI_API_KEY", None)  # Lee clave desde settings
        if not api_key:  # Si no hay clave
            raise RuntimeError("GEMINI_API_KEY no configurado en settings.")  # Error descriptivo
        genai.configure(api_key=api_key)  # Configura el cliente
        # Usa el modelo rápido para análisis
        self.model = genai.GenerativeModel("gemini-1.5-flash")  # Selecciona modelo

    def analyze_comment(self, text: str) -> dict:  # Analiza un comentario de usuario
        """Analiza sentimiento y toxicidad, devolviendo estructura JSON."""  # Documenta el método
        # Construimos un prompt pidiendo salida JSON explícita
        prompt = (
            "Responde en JSON con las claves: sentiment (positivo|negativo|neutral), "
            "toxicity (0-1), explanation (breve). Texto: " + text
        )  # Prompt detallado
        result = self.model.generate_content(prompt)  # Genera contenido con Gemini
        # Intentamos parsear JSON si el modelo lo devuelve como texto JSON
        try:  # Intenta interpretación directa
            import json  # Importa JSON

            parsed = json.loads(result.text)  # Parsea el texto como JSON
            # Asegura claves mínimas
            return {
                "sentiment": parsed.get("sentiment"),  # Sentimiento
                "toxicity": parsed.get("toxicity"),  # Toxicidad
                "explanation": parsed.get("explanation"),  # Explicación
                "raw": result.text,  # Texto crudo por transparencia
            }  # Devuelve estructura
        except Exception:  # Si no es JSON
            return {  # Devuelve texto crudo con una estimación básica
                "sentiment": None,  # No determinado
                "toxicity": None,  # No determinado
                "explanation": None,  # No determinado
                "raw": result.text,  # Texto devuelto por el modelo
            }  # Estructura alternativa

    def ask_question(self, question: str) -> dict:  # Responde preguntas del admin
        """Envía una pregunta libre al modelo y devuelve texto."""  # Documenta el método
        result = self.model.generate_content(question)  # Genera la respuesta
        return {"answer": getattr(result, "text", ""), "raw": getattr(result, "text", "")}  # Estructura simple