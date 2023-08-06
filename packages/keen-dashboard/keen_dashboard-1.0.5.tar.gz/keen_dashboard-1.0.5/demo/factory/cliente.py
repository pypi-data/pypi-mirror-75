import factory

from ..models import Cliente


class ClienteFactory(factory.Factory):
    class Meta:
        model = Cliente
