from odoo import models, fields, api
from collections import Counter

class PosSession(models.Model):
    _inherit = 'pos.session'

    summary_total_sales = fields.Monetary(
        string="Total de Ventas del Turno",
        compute='_compute_session_summary',
        store=True,
        readonly=True
    )
    summary_top_products = fields.Text(
        string="Productos Más Vendidos",
        compute='_compute_session_summary',
        store=True,
        readonly=True
    )
    summary_active_time = fields.Char(
        string="Tiempo Activo del Turno",
        compute='_compute_session_summary',
        store=True,
        readonly=True
    )

    @api.depends('order_ids.state', 'start_at', 'stop_at')
    def _compute_session_summary(self):
        for session in self:
            session.summary_total_sales = sum(order.amount_total for order in session.order_ids if order.state != 'cancel')
            product_counts = Counter()
            for order in session.order_ids.filtered(lambda o: o.state != 'cancel'):
                for line in order.lines:
                    product_counts[line.product_id.display_name] += line.qty
            top_products_list = [f"- {product}: {int(qty)}" for product, qty in product_counts.most_common(5)]
            session.summary_top_products = "\n".join(top_products_list) if top_products_list else "No se vendieron productos."
            if session.start_at and session.stop_at:
                duration = session.stop_at - session.start_at
                hours, remainder = divmod(duration.total_seconds(), 3600)
                minutes, _ = divmod(remainder, 60)
                session.summary_active_time = f"{int(hours)} horas y {int(minutes)} minutos"
            else:
                session.summary_active_time = "Sesión en curso"

    def action_pos_session_closing_control(self, balancing_account=False, amount_to_balance=0, bank_payment_method_diffs=None):
        # Primero, calculamos y guardamos nuestro resumen
        self._compute_session_summary()
        # Luego, llamamos al método original y devolvemos lo que sea que devuelva.
        # Esto permite que el flujo normal del TPV continúe sin interrupciones.
        res = super(PosSession, self).action_pos_session_closing_control(balancing_account, amount_to_balance, bank_payment_method_diffs)
        return res