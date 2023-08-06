import factory

from demo.models import Pedido


class PedidoFactory(factory.Factory):
    class Meta:
        model = Pedido
