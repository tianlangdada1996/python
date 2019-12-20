
from django.shortcuts import render,redirect,HttpResponse
from rbac import models
from django.conf import settings
from rbac.serve.permission_insert import init_permission


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

            #权限注入
            init_permission(request,uname)
            # [{'permissions__url': '/customer/add/'},]

            return redirect('/customer/list/')
        else:
            return redirect('/login/')














