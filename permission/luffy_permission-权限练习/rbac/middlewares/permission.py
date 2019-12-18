import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, HttpResponse


class Auth(MiddlewareMixin):

    def process_request(self, request):

        white_list = [
            '^/login/$',
            '^/admin.*$'
        ]

        current_path = request.path
        for path in white_list:
            if re.match(path, current_path):
                break
        else:
            if request.session.get("username"):
                permission_list = request.session.get("permission_list")
                for permission in permission_list:
                    path = '^%s$' % permission['url']
                    if re.match(path, current_path):
                        pid = permission["parent_id"]
                        if pid:
                            request.pid = pid
                        else:
                            request.pid = permission["id"]
                        # print(request.pid)
                        break
                else:
                    return HttpResponse("您没有权限访问！")
            else:
                return redirect("login")
