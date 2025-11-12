from rest_framework.views import APIView
from rest_framework.response import Response
from ..services.firebase_client import FirestoreClient


class FirebaseTestView(APIView):
    """Prueba de conexión con Firestore (sin Cloud Functions)."""

    def get(self, request):
        fc = FirestoreClient()
        events = fc.get_events(limit=5)
        return Response({"ok": True, "count": len(events), "sample": events})