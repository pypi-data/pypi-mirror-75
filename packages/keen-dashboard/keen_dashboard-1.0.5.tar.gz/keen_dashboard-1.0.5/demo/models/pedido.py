from django.db.models import *


class Pedido(Model):
    cliente = ForeignKey('demo.Cliente', null=True, on_delete=SET_NULL)
    valor = DecimalField(max_length=10, max_digits=10, decimal_places=2)
    data = DateField(auto_now=True)

    class Meta:
        db_table = 'pedido'
        app_label = 'demo'
