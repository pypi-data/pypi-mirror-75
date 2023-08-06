from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField


class Usuario(AbstractUser):
    avatar = ImageField(null=True)

    class Meta:
        db_table = 'usuario'