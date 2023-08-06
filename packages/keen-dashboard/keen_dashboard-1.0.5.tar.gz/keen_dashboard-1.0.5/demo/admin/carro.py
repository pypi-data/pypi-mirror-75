from functools import wraps

from demo.models import Cliente
from keen_dashboard.admin import KeenModelAdmin


def cliente_decorador(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        extra_context = kwargs.get('extra_context', {})
        cliente = Cliente.objects.get(pk=kwargs['cliente_id'])
        extra_context.update({
            'cliente': cliente,
            'parent_breadcrumbs': (
                ('Lista de Clientes', 'admin:demo_cliente_changelist'),
                (str(cliente), 'admin:demo_cliente_change')
            )
        })
        kwargs.update({'extra_context': extra_context})
        return function(request, *args, **kwargs)

    return wrap


class CarroAdmin(KeenModelAdmin):
    fields = 'modelo', 'placa'

    def save_model(self, request, obj, form, change):
        obj.cliente = Cliente.objects.get(pk=request.resolver_match.kwargs['cliente_id'])
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request)

    @cliente_decorador
    def changelist_view(self, request, cliente_id=None, extra_context=None):
        return super().changelist_view(request, extra_context)

    @cliente_decorador
    def change_view(self, request, cliente_id, object_id=None, form_url='', extra_context=None):
        return super().change_view(request, object_id, form_url, extra_context)

    @cliente_decorador
    def delete_view(self, request, cliente_id, object_id=None, extra_context=None):
        return super().delete_view(request, object_id, extra_context)

    @cliente_decorador
    def history_view(self, request, cliente_id, object_id=None, extra_context=None):
        return super().history_view(request, object_id, extra_context)

    @cliente_decorador
    def add_view(self, request, cliente_id=None, form_url='', extra_context=None):
        return super().add_view(request, form_url, extra_context)
