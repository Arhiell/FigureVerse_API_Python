from datetime import datetime  # Utilidad de fechas
from typing import Any, Optional  # Tipos opcionales

from django.db import transaction  # Manejo de transacciones DB (se usa solo para atomicidad local)
from django.utils import timezone  # Manejo de zonas horarias

from ..services.firebase_client import FirestoreClient  # Cliente para Firestore


def _parse_timestamp(value: Any) -> Optional[datetime]:  # Parsea diferentes formatos de timestamp
    """Convierte timestamp (datetime, epoch, ISO string) a datetime aware."""  # Documenta la función
    if value is None:  # Si es nulo
        return None  # No se puede parsear
    if isinstance(value, datetime):  # Si ya es datetime
        return value if timezone.is_aware(value) else timezone.make_aware(value)  # Asegura tz-aware
    if isinstance(value, (int, float)):  # Si es epoch
        return timezone.make_aware(datetime.fromtimestamp(value))  # Convierte a datetime con tz
    if isinstance(value, str):  # Si es string ISO
        try:  # Intenta parsear
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))  # Reemplaza Z por +00:00
            return dt if timezone.is_aware(dt) else timezone.make_aware(dt)  # Asegura tz-aware
        except Exception:  # Si falla
            return None  # Devuelve None
    return None  # Formato no soportado


def run_sync(limit: int = 50) -> int:  # Procesa eventos y publica métricas en Firestore
    """Lee eventos desde Firestore y actualiza métricas en Firestore (sin DB local)."""  # Documenta la función
    fc = FirestoreClient()  # Inicializa cliente Firestore

    events = fc.get_recent_events(limit)  # Lee eventos recientes
    new_count = 0  # Contador de eventos procesados

    product_totals: dict[str, float] = {}  # Acumulador de ventas por producto

    with transaction.atomic():  # Agrupa operaciones (aunque toda persistencia es en Firestore)
        for e in events:  # Itera cada evento
            ts = _parse_timestamp(e.get("timestamp"))  # Parsea timestamp
            payload = e.get("payload", {})  # Payload
            event_type = e.get("event") or e.get("type")  # Tipo

            # Procesa ventas
            if event_type in ["OrderCreated", "PaymentApproved"]:  # Eventos de venta
                for p in payload.get("productos", []):  # Lista de productos
                    pid = p.get("id") or p.get("id_producto")  # Id producto
                    precio = float(p.get("precio", 0))  # Precio
                    if not pid:  # Validación
                        continue  # Salta
                    product_totals[pid] = product_totals.get(pid, 0.0) + precio  # Acumula

            # Procesa eventos de producto (marca último evento)
            if event_type in ["ProductCreated", "ProductUpdated"]:  # Eventos de producto
                pid = payload.get("id_producto") or payload.get("id")  # Id
                if pid:  # Si existe
                    fc.upsert_product_stat(pid, {"product_id": pid, "last_event": event_type})  # Upsert

            new_count += 1  # Incrementa contador

        # Publica totales por producto
        for pid, ventas in product_totals.items():  # Itera acumulados
            fc.upsert_product_stat(pid, {"product_id": pid, "sales_total": ventas})  # Upsert

        # Publica overview básico
        fc.set_analytics_overview({
            "total_ventas": sum(product_totals.values()),  # Suma total
            "total_productos": len(product_totals),  # Conteo
        })  # Guarda overview

    return new_count  # Devuelve cantidad de eventos procesados


def _process_sales_event(payload: dict, event_type: str) -> None:  # Obsoleto (use run_sync)
    """Mantenido por compatibilidad; la lógica principal está en run_sync."""


def _process_product_event(payload: dict, event_type: str) -> None:  # Obsoleto (use run_sync)
    """Mantenido por compatibilidad; la lógica principal está en run_sync."""