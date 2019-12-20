from django import template

register = template.Library()


@register.inclusion_tag("module/menus.html")
def menus(request):
    menu_list = request.session.get("menu_list")
    for menu in menu_list:
        menu['class'] = 'hidden'
        for path in menu['children']:
            # if path['url'] == current_path:
            path['class'] = ''
            if request.pid == path['id']:  #
                menu['class'] = ''
                path['class'] = 'active'
    return {"menu_list": menu_list}


@register.inclusion_tag("module/bread_crumb.html")
def bread_crumb(request):
    crumb = request.session.get("bread_crumb")
    return {"bread_crumb":crumb}
