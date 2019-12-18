
from django.shortcuts import render,redirect,HttpResponse
from rbac import models
from django.conf import settings

def login(request):

    if request.method == 'GET':
        return render(request, 'login.html')

    else:
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        user_obj = models.UserInfo.objects.filter(
            username=uname,
            password=pwd
        )

        if user_obj:
            # 登录成功
            request.session['is_login'] = True

            # 往session中注入权限
            permission_list = models.Role.objects.filter(userinfo__username=uname).values(
                'permissions__id',
                'permissions__is_menu',
                'permissions__url',
                'permissions__title',
                'permissions__icon',
            ).distinct()

            menu_list = []  #[{permission__url:'/xx/list/'}]

            for permission in permission_list:
                if permission['permissions__is_menu']:
                    menu_list.append(permission)
            print(permission_list)

            # <QuerySet [{'permissions__url': '/customer/list/'}, {'permissions__url': '/customer/add/'}, {'permissions__url': '/customer/edit/(?P<cid>\\d+)/'}]>

            request.session[settings.PERMISSION_KEY] = list(permission_list)
            request.session[settings.MENU_KEY] = menu_list

            # [{'permissions__url': '/customer/add/'},]

            return redirect('/customer/list/')
        else:
            return redirect('/login/')

