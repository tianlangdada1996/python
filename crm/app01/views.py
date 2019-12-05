from django.shortcuts import render, redirect, HttpResponse
from django.views import View

from . import models
from . import crmforms
from crmtools import encryption


# Create your views here.
class Login(View):

    def get(self, request):
        login = crmforms.Login()
        return render(request, "identity/login.html", {"forms_obj": login})

    def post(self, request):
        login = crmforms.Login(data=request.POST)
        if login.is_valid():
            return HttpResponse("OK")
        else:
            return render(request, "identity/login.html", {"forms_obj": login})


class Register(View):

    def get(self, request):
        register = crmforms.Register()
        return render(request, "identity/register.html", {"forms_obj": register})

    def post(self, request):
        register = crmforms.Register(data=request.POST)
        if register.is_valid():
            user_data = register.cleaned_data
            user_data.pop("confirm_password")
            user_data['password'] = encryption.encryption(user_data['username'], user_data['password'])
            models.UserInfo.objects.create(
                **user_data
            )
            return redirect("app01:login")
        else:
            return render(request, "identity/register.html", {"forms_obj": register})
