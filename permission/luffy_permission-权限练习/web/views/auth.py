from django.shortcuts import render, redirect
from django.views import View

from rbac import models


class Login(View):

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        user = request.POST.get("username")
        pwd = request.POST.get("password")
        user_obj = models.UserInfo.objects.filter(username=user, password=pwd)
        if user_obj:
            request.session['username'] = user
            permission_list = models.Permission.objects.filter(role__userinfo__username=user).values()
            # print(permission_list)
            permission_dict = {permission['id']: permission for permission in permission_list}
            # print(permission_dict)
            request.session["permission_dict"] = permission_dict
            # menu_list = permission_list.filter(menu__isnull=False)
            url_name = [permission['url_name'] for permission in permission_list]
            print(url_name)
            request.session['url_name'] = url_name

            first_level_menus = models.FirstLevelMenu.objects.filter(permission__role__userinfo__username=user).distinct().order_by('-weight')
            menu_list = list(first_level_menus.values("id", "title", "icon"))
            for index, first_level_menu in enumerate(first_level_menus):
                second_level_menus = list(models.Permission.objects.filter(menu=first_level_menu, role__userinfo__username=user).values())
                menu_list[index]["children"] = second_level_menus
            # print(menu_list)

            request.session["menu_list"] = menu_list

            return redirect("/customer/list/")
        else:
            return redirect("login")
