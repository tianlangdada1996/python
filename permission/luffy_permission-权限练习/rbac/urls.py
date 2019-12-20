from django.conf.urls import url
from rbac import views

urlpatterns = [
    url(r'^permission/role/list/$', views.rolelist, name="role_list"),
    url(r'^permission/role/add/$', views.RoleAddEdit.as_view(), name="role_add"),
    url(r'^permission/role/edit/(\d+)/$', views.RoleAddEdit.as_view(), name="role_edit"),
    url(r'^permission/role/del/(\d+)/$', views.roledel, name="role_del"),
    url(r'^permission/menu/list/$', views.MenuList.as_view(), name="menu_list"),
]