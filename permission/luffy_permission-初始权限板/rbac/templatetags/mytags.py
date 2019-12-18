from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    current_path = request.path
    menu_list = request.session.get(settings.MENU_KEY)
    # menu = {'permissions__url','permissions__title'}
    for menu in menu_list:
        if menu['permissions__url'] == current_path:
            menu['class'] = 'active'

    return {'menu_list': menu_list}

