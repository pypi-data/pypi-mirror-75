from django.db.models import *
from django.utils.timezone import now

STATUS_CLIENTE = (
    (1, 'Cliente Status 1'),
    (2, 'Cliente Status 2'),
    (3, 'Cliente Status 3'),
    (4, 'Cliente Status 4'),
)


class Cliente(Model):
    nome = CharField(max_length=30)
    descricao = TextField(default='')
    status = IntegerField(choices=STATUS_CLIENTE, default=1)
    data_cadastro = DateTimeField(null=True, default=now)
    hora_cadastro = TimeField(null=True)
    avatar = ImageField(null=True)

    def __str__(self):
        return str(self.nome)

    class Meta:
        db_table = 'cliente'
        app_label = 'demo'