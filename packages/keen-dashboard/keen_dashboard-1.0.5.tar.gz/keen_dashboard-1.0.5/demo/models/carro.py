from django.db.models import *


class Carro(Model):
    modelo = CharField(max_length=20)
    placa = CharField(max_length=10)
    cliente = ForeignKey('demo.Cliente', on_delete=SET_NULL, null=True)

    def __str__(self):
        return str(self.modelo) + ' - ' + str(self.placa)

    class Meta:
        db_table = 'carro'
        app_label = 'demo'