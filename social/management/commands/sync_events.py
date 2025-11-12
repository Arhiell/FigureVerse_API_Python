from django.core.management.base import BaseCommand

from ...tasks.sync_events import run_sync


class Command(BaseCommand):
    help = "Procesa eventos recientes de Firestore y publica métricas en /analytics y /product_stats."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=50,
            help="Cantidad de eventos recientes a procesar",
        )

    def handle(self, *args, **options):
        limit = options.get("limit", 50)
        try:
            processed = run_sync(limit=limit)
            self.stdout.write(self.style.SUCCESS(f"Eventos procesados: {processed}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error procesando eventos: {e}"))