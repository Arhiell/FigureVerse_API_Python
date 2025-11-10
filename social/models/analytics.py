"""
Modelos derivados/agregados para analítica .

Inicialmente un único modelo opcional: ProductAnalytics, que guarda
pre-agregados por producto (ventas e ingresos acumulados).
"""

from django.db import models


class ProductAnalytics(models.Model):
    """
    Guarda agregados precalculados (ventas totales, ingresos totales por
    producto). Útil para acelerar consultas de dashboard si los cálculos
    en tiempo real son costosos.
    """
    product_id = models.IntegerField()
    total_sales = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ProductAnalytics(product={self.product_id}, sales={self.total_sales}, revenue={self.total_revenue})"