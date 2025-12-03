from django.apps import AppConfig
import threading


_started = False


class FeedbackConfig(AppConfig):
    name = "feedback"

    def ready(self):
        global _started
        if _started:
            return
        _started = True
        from .services.analysis_service import analyze_general_opinion_for_products
        t = threading.Thread(target=analyze_general_opinion_for_products, daemon=True)
        t.start()
