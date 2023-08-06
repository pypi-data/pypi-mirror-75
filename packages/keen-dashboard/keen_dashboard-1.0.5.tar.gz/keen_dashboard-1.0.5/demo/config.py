from django.templatetags.static import static
from django.urls import reverse

from keen_dashboard.config import KeenConfig


class AdminConfig(KeenConfig):

    @staticmethod
    def get_app_info(request):
        data = {
            'logo': static('src/assets/media/logos/logo-4.png'),
            'logo_url': '/',
            'logo_sticky': static('src/assets/media/logos/logo-4.png'),
            'title': 'App title',
            'fluid': True,
            'display_footer': False,
        }
        return data

    @staticmethod
    def get_header_menu(request):
        data = {
            'menus': [
                ('Empresa', {
                    'icon': 'fas fa-car',
                    'url': '#',
                    'has_perm': True,
                    'children': (
                        ('Clientes', {
                            'icon': 'fas fa-file',
                            'url': '/admin/demo/cliente/',
                            'has_perm': True
                        }),
                        ('Pedidos', {
                            'icon': 'fas fa-calendar',
                            'url': '/admin/demo/pedido/',
                            'has_perm': True
                        }),

                    )
                }),
                ('Pedidos', {
                    'icon': 'fas fa-key',
                    'url': '/',
                    'has_perm': True,
                })
            ]
        }
        return data

    @staticmethod
    def get_user_menu(request):
        data = {
            'user_name': request.user.username,
            'user_subtitle': 'Admin',
            'user_avatar': None,
            'user_avatar_color': 'primary',
            'user_initials': str(request.user.username[0:2]).upper(),
            'user_menus': (
                ('Alterar Senha', {
                    'icon': 'fas fa-search',
                    'url': reverse('admin:password_change'),
                    'has_perm': True
                }
                 ),
            ),
            'signout_url': reverse('admin:logout'),
        }
        return data

    @staticmethod
    def get_user_apps(request):
        apps = {
            'user_apps': [
                ('Clientes', {
                    'label': 'Separa um pdf contendo vários CAMS, em vários PDFs menores. Divididos por bitola.',
                    'url': '/extrator/pdf/add/',
                    'image': static('dist/assets/media/users/300_16.jpg'),
                    'has_perm': True,
                }),
                ('Carros', {
                    'label': 'Separa um pdf contendo vários CAMS, em vários PDFs menores. Divididos por bitola.',
                    'url': '/extrator/pdf/add/',
                    'image': static('dist/assets/media/users/300_16.jpg'),
                    'has_perm': True,
                }),
                ('Pedidos', {
                    'label': 'Separa um pdf contendo vários CAMS, em vários PDFs menores. Divididos por bitola.',
                    'url': '/extrator/pdf/add/',
                    'image': static('dist/assets/media/users/300_16.jpg'),
                    'has_perm': True,
                })
            ],
        }
        return apps
