import firebase_admin  # SDK de Firebase para Python
from firebase_admin import credentials, firestore  # Módulos para credenciales y Firestore
from django.conf import settings  # Acceso a configuración de Django


class FirestoreClient:  # Cliente para interactuar con Firestore
    def __init__(self):  # Inicializa el cliente
        # Si no hay apps Firebase inicializadas, inicializa con credenciales del archivo JSON
        if not firebase_admin._apps:  # Verifica si ya existe una app de Firebase
            cred = credentials.Certificate(settings.GOOGLE_APPLICATION_CREDENTIALS)  # Carga credenciales
            init_opts = {}  # Opciones de inicialización
            if getattr(settings, "FIREBASE_PROJECT_ID", None):  # Si hay projectId en settings
                init_opts["projectId"] = settings.FIREBASE_PROJECT_ID  # Usa ese projectId
            firebase_admin.initialize_app(cred, init_opts)  # Inicializa la app de Firebase
        self.db = firestore.client()  # Crea el cliente de Firestore

    def get_events(self, limit: int = 10):  # Obtiene eventos (ordenados por timestamp)
        """Lee los últimos N eventos desde Firestore por campo 'timestamp'."""  # Documenta función
        try:  # Intenta realizar consulta ordenada
            query = (  # Construye la query
                self.db.collection("events")  # Colección 'events'
                .order_by("timestamp", direction=firestore.Query.DESCENDING)  # Ordena por timestamp desc
                .limit(limit)  # Limita cantidad de documentos
            )
            docs = []  # Lista de resultados
            for doc in query.stream():  # Itera documentos del cursor
                data = doc.to_dict() or {}  # Convierte a diccionario
                data.setdefault("external_id", doc.id)  # Asegura incluir el id del doc como external_id
                data.setdefault("id", doc.id)  # También como id
                docs.append(data)  # Agrega al resultado
            return docs  # Devuelve lista de eventos
        except Exception:  # Si falla el orden (p.ej. índice no creado)
            docs = []  # Lista de resultados sin orden
            for doc in self.db.collection("events").limit(limit).stream():  # Consulta sin order_by
                data = doc.to_dict() or {}  # Convierte a diccionario
                data.setdefault("external_id", doc.id)  # Incluye id del documento
                data.setdefault("id", doc.id)  # Incluye id del documento
                docs.append(data)  # Agrega al resultado
            return docs  # Devuelve resultados

    def get_recent_events(self, limit: int = 50):  # Obtiene los eventos más recientes
        """Obtiene los últimos eventos ordenados por timestamp."""  # Documenta función
        return self.get_events(limit=limit)  # Reutiliza la lógica de get_events

    # ==== Lectura/Escritura en colecciones de analítica ====
    def get_analytics_overview(self) -> dict:  # Lee overview desde '/analytics/overview'
        """Lee el documento 'overview' de la colección analytics."""  # Documenta función
        doc_ref = self.db.collection("analytics").document("overview")  # Referencia al doc overview
        snap = doc_ref.get()  # Obtiene snapshot
        return snap.to_dict() or {}  # Devuelve dict o vacío

    def set_analytics_overview(self, data: dict) -> None:  # Escribe overview en '/analytics/overview'
        """Guarda el documento 'overview' en analytics (merge)."""  # Documenta función
        self.db.collection("analytics").document("overview").set(data, merge=True)  # Upsert con merge

    def get_top_product_stats(self, limit: int = 10) -> list[dict]:  # Top por reputación
        """Lee top de productos desde '/product_stats' ordenando por 'reputation_index'."""  # Documenta función
        query = (
            self.db.collection("product_stats")  # Colección de estadísticas por producto
            .order_by("reputation_index", direction=firestore.Query.DESCENDING)  # Orden desc
            .limit(limit)  # Límite
        )
        items = []  # Acumulador
        for doc in query.stream():  # Itera resultados
            data = doc.to_dict() or {}  # Convierte a dict
            data.setdefault("product_id", doc.id)  # Asegura id
            items.append(data)  # Agrega
        return items  # Devuelve lista

    def upsert_product_stat(self, product_id: str, data: dict) -> None:  # Guarda métricas de producto
        """Crea/actualiza un documento en '/product_stats/{product_id}'."""  # Documenta función
        self.db.collection("product_stats").document(product_id).set(data, merge=True)  # Upsert

    def add_comment(self, comment: dict) -> str:  # Agrega comentario en '/comments'
        """Crea un documento en la colección 'comments' y devuelve su id."""  # Documenta función
        ref = self.db.collection("comments").add(comment)[1]  # add devuelve (update_time, ref)
        return ref.id  # Devuelve id del doc

    def add_ai_insight(self, insight: dict) -> str:  # Agrega resultado de IA
        """Crea un documento en la colección 'ai_insights' y devuelve su id."""  # Documenta función
        ref = self.db.collection("ai_insights").add(insight)[1]  # Crea doc
        return ref.id  # Devuelve id

    # ==== Utilidades de recálculo ====
    def aggregate_from_events(self) -> tuple[dict, dict]:  # Calcula overview y stats por producto
        """Lee eventos y calcula métricas (ventas por producto y overview)."""  # Documenta función
        events = self.get_recent_events(limit=1000)  # Lee hasta 1000 recientes (ajustable)
        product_totals: dict[str, float] = {}  # Ventas acumuladas por producto
        for e in events:  # Itera eventos
            etype = e.get("event") or e.get("type")  # Tipo de evento
            payload = e.get("payload", {})  # Payload
            if etype in ["OrderCreated", "PaymentApproved"]:  # Eventos de venta
                for p in payload.get("productos", []):  # Lista de productos
                    pid = p.get("id") or p.get("id_producto")  # Id producto
                    precio = float(p.get("precio", 0))  # Precio
                    if not pid:  # Si falta id
                        continue  # Salta
                    product_totals[pid] = product_totals.get(pid, 0.0) + precio  # Acumula

        # Construye overview
        total_ventas = sum(product_totals.values())  # Suma total
        total_productos = len(product_totals)  # Cantidad distinta
        overview = {  # Documento overview
            "total_ventas": total_ventas,
            "total_productos": total_productos,
            "generated_at": firestore.SERVER_TIMESTAMP,  # Marca temporal del servidor
        }
        # Construye documents de product_stats con ventas_total
        product_stats_docs: dict[str, dict] = {}  # Mapa product_id -> doc
        for pid, ventas in product_totals.items():  # Itera acumulados
            product_stats_docs[pid] = {
                "product_id": pid,
                "sales_total": ventas,
                "updated_at": firestore.SERVER_TIMESTAMP,
            }  # Solo ventas por ahora; reputación vendrá de IA/comentarios
        return overview, product_stats_docs  # Devuelve overview y mapa de stats