import re

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect,render,HttpResponse

class Auth(MiddlewareMixin):

    def process_request(self,request):

        # 登录认证白名单
        white_list = ['/login/','/admin/.*']
        # 登录认证

        current_path = request.path
        for i in white_list:
            if re.match(i,current_path):
                break
        else:
            is_login = request.session.get('is_login')
            if not is_login:
                return redirect('/login/')

            else:

                # 权限认证
                permission_list = request.session.get(settings.PERMISSION_KEY)

                # re.match('/customer/edit/(?P<cid>\d+)/',customer/edit/2/)
                #/customer/edit/(?P<cid>\d+)/  -- customer/edit/2/
                for permission in permission_list: #[{'url':'/custer/'}]
                    # if current_path == permission['permissions__url']:
                    reg = r'^%s$'%permission['permissions__url']
                    if re.match(reg,current_path):  #/customer/add/
                        pid = permission['permissions__parent_id'] #None
                        if pid:
                            request.pid = pid  #wsgihttprequest对象
                            print(request.pid)
                        else:
                            request.pid = permission['permissions__id']

                        return
                else:
                    return HttpResponse('您不配!!!')







