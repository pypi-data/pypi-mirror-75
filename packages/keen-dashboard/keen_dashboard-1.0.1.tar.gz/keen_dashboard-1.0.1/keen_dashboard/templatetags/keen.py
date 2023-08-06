from django import template
from django.templatetags.static import static

register = template.Library()


@register.inclusion_tag('admin/includes/apps.html')
def user_apps(request):
    apps = {
        'user_apps': [
            ('Separar PDF', {
                'label': 'Separa um pdf contendo vários CAMS, em vários PDFs menores. Divididos por bitola.',
                'url': '/extrator/pdf/add/',
                'image': static('dist/assets/media/users/300_16.jpg'),
                'has_perm': True,
            }),
            ('Separar PDF', {
                'label': 'Separa um pdf contendo vários CAMS, em vários PDFs menores. Divididos por bitola.',
                'url': '/extrator/pdf/add/',
                'image': static('dist/assets/media/users/300_16.jpg'),
                'has_perm': True,
            }),
            ('Separar PDF', {
                'label': 'Separa um pdf contendo vários CAMS, em vários PDFs menores. Divididos por bitola.',
                'url': '/extrator/pdf/add/',
                'image': static('dist/assets/media/users/300_16.jpg'),
                'has_perm': True,
            }),
            ('Separar PDF', {
                'label': 'Separa um pdf contendo vários CAMS, em vários PDFs menores. Divididos por bitola.',
                'url': '/extrator/pdf/add/',
                'image': static('dist/assets/media/users/300_16.jpg'),
                'has_perm': True,
            }),
        ],
    }
    return apps


@register.inclusion_tag('admin/includes/user_menu.html')
def user_menu(request):
    data = {
        'user_name': 'Jon Doe',
        'user_subtitle': 'Admin',
        'user_avatar': static('src/assets/media/users/300_25.jpg'),
        'user_menus': (
            ('My Profile', {
                'icon': 'fas fa-search',
                'url': '#',
                'has_perm': True
            }
             ),
        ),
        'signout_url': '#',
    }

    return data


@register.simple_tag()
def app_info(request):
    data = {
        'logo': static('src/assets/media/logos/logo-4.png'),
        'logo_url': '/',
        'logo_sticky': static('src/assets/media/logos/logo-4.png'),
        'title': 'Foo Bar',
        'fluid': True,
        'display_footer': False,
    }
    return data


@register.inclusion_tag('admin/includes/header_menu.html')
def header_menu(request):
    data = {
        'menus': [
            ('Dobra', {
                'icon': 'fas fa-adjust',
                'url': '#',
                'has_perm': request.user.has_perm('core.config') or request.user.is_superuser,
                'children': (
                    ('Menu 1', {
                        'icon': 'fas fa-file',
                        'url': 'teste',
                        'has_perm': True
                    }),
                    ('Menu 2', {
                        'icon': 'fas fa-circle',
                        'url': '#',
                        'has_perm': True
                    }),
                )
            }),
            ('Menu 2', {
                'icon': 'flaticon-map',
                'url': '#',
                'has_perm': True,
            })
        ]
    }
    return data
