from django.contrib import admin
from django.urls import reverse_lazy

from demo.models import Pedido
from keen_dashboard.admin import KeenModelAdmin


@admin.register(Pedido)
class PedidoAdmin(KeenModelAdmin):
    raw_id_fields_attrs = {
        'cliente': {
            'url': reverse_lazy('admin:demo_cliente_changelist'),
            'field': 'action-select'
        }
    }
    list_per_page = 30
    raw_id_fields = 'cliente',
