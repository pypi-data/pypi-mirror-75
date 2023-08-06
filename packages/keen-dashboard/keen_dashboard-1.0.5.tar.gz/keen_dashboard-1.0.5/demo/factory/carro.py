import factory

from ..models import Carro


class CarroFactory(factory.Factory):
    class Meta:
        model = Carro
