"""
Servicio de negocio para analítica.

Integra datos de pedidos (Node) y, a futuro, datos propios (ratings,
comentarios) para construir métricas del dashboard.
"""

from typing import List, Dict, Any, Tuple
from collections import defaultdict

from social.repositories.order_repository import OrderRepository


class AnalyticsService:
    """
    Calcula métricas de top productos y overview a partir de órdenes.
    """

    @staticmethod
    def _extract_items(order: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrae la lista de ítems de una orden con tolerancia a nombres de
        campos. Se espera que cada ítem contenga:
        - product_id (o 'product' con 'id')
        - quantity (o 'qty')
        - unit_price (o 'price')
        """
        items = order.get('items') or []
        normalized = []
        for item in items:
            # product_id
            pid = item.get('product_id')
            if pid is None:
                product = item.get('product') or {}
                pid = product.get('id')

            # quantity
            qty = item.get('quantity')
            if qty is None:
                qty = item.get('qty')

            # unit price
            price = item.get('unit_price')
            if price is None:
                price = item.get('price')

            if pid is None or qty is None or price is None:
                # Ítem incompleto; lo omitimos
                continue

            normalized.append({
                'product_id': pid,
                'quantity': qty,
                'unit_price': price,
            })
        return normalized

    @staticmethod
    def top_products(range_days: int = 30, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Construye ranking por ingresos (desc), incluyendo ventas totales.
        Nota: En esta fase no filtramos por fecha real; el parámetro es
        aceptado como placeholder para el pipeline futuro.
        """
        orders = OrderRepository.get_orders()
        revenue_by_product: Dict[int, float] = defaultdict(float)
        sales_by_product: Dict[int, int] = defaultdict(int)

        for order in orders:
            for item in AnalyticsService._extract_items(order):
                revenue_by_product[item['product_id']] += item['quantity'] * float(item['unit_price'])
                sales_by_product[item['product_id']] += item['quantity']

        ranking = [
            {
                'product_id': pid,
                'total_revenue': round(revenue_by_product[pid], 2),
                'total_sales': sales_by_product[pid],
            }
            for pid in revenue_by_product.keys()
        ]

        ranking.sort(key=lambda x: x['total_revenue'], reverse=True)
        return ranking[:limit]

    @staticmethod
    def overview() -> Dict[str, Any]:
        """
        Calcula métricas globales: órdenes_totales, ingresos_totales, items_totales.
        """
        orders = OrderRepository.get_orders()
        total_orders = len(orders)
        total_revenue = 0.0
        total_items = 0

        for order in orders:
            for item in AnalyticsService._extract_items(order):
                total_revenue += item['quantity'] * float(item['unit_price'])
                total_items += item['quantity']

        return {
            'orders_totales': total_orders,
            'ingresos_totales': round(total_revenue, 2),
            'items_totales': total_items,
        }