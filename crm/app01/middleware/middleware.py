import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse

from app01 import models


class Auth(MiddlewareMixin):
    white_list = [
        reverse("app01:login"),
        reverse("app01:register"),
        "/admin.*"
    ]

    def process_request(self, request):
        for re_path in self.white_list:
            if re.search(re_path, request.path):
                break
        else:
            user = request.session.get("username")
            ret = models.UserInfo.objects.filter(username=user)
            if not ret:
                return redirect('app01:login')
