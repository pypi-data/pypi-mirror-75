from django.contrib import admin
from django.forms import ModelForm, FileField, CharField
from django.urls import include, path

from demo.admin import CarroAdmin
from demo.models import Cliente, Carro
from keen_dashboard.admin import KeenModelAdmin
from keen_dashboard.templatetags.admin_utils import admin_url
from keen_dashboard.widgets import AdminAvatarWidget, EnclosedWidget


class FormCliente(ModelForm):
    avatar = FileField(widget=AdminAvatarWidget)
    nome = CharField(widget=EnclosedWidget(append='fas fa-car', prepend='fas fa-circle'))


@admin.register(Cliente)
class ClienteAdmin(KeenModelAdmin):
    form = FormCliente

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = {
            'extra_object_tools': (
                ('Carros', {
                    'url': admin_url(request, 'admin:demo_carro_changelist'),
                    'icon': 'fas fa-circle',
                    'has_perm': True
                }),
            )
        }
        return super().change_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        urls_carro = CarroAdmin(model=Carro, admin_site=admin.site).get_urls()
        urls = [path('<cliente_id>/carros/', include(urls_carro))]
        urls += super().get_urls()
        return urls
