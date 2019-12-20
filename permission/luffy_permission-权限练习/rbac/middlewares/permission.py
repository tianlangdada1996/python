import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, HttpResponse


class Auth(MiddlewareMixin):

    def process_request(self, request):

        white_list = [
            '^/login/$',
            '^/admin.*$'
        ]

        bread_crumb = [
            {'title': '首页', 'url': 'javascript:void(0);'},
        ]

        current_path = request.path
        for path in white_list:
            if re.match(path, current_path):
                break
        else:
            if request.session.get("username"):
                permission_dict = request.session.get("permission_dict")
                for permission in permission_dict.values():
                    path = '^%s$' % permission['url']
                    if re.match(path, current_path):
                        pid = permission["parent_id"]
                        if pid:
                            bread_crumb.append({"title": permission_dict[str(pid)]["title"],
                                                "url": permission_dict[str(pid)]["url"]})
                            bread_crumb.append({"title": permission['title'],
                                                "url": permission["url"]})
                            request.pid = pid
                        else:
                            bread_crumb.append({"title":permission['title'],
                                                "url":permission["url"]})
                            request.pid = permission["id"]
                        # print(request.pid)
                        request.session["bread_crumb"] = bread_crumb

                        break
                else:
                    return HttpResponse("您没有权限访问！")
            else:
                return redirect("login")
