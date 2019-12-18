import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "luffy_permission.settings")

    import django

    django.setup()

    from rbac import models
    from django.db.models import *

    permission_list = models.Permission.objects.filter(role__userinfo__username="yzm")
    # print(permission_list)
    # first_level_menus = models.FirstLevelMenu.objects.filter(permission__role__userinfo__username="yzm").distinct().order_by('weight')
    # menus = list(first_level_menus.values("id", "title", "icon"))
    # for index, first_level_menu in enumerate(first_level_menus):
    #     second_level_menus = list(models.Permission.objects.filter(menu=first_level_menu, role__userinfo__username="yzm").values())
    #     menus[index]["children"] = second_level_menus
    # print(menus)
