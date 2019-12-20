from django.conf.urls import url,include
from rbac import views

urlpatterns = [
    # /rbac/role/list

    url(r'^role/list/', views.role_list,name='role_list'),
    url(r'^role/add/', views.role_add_edit,name='role_add'),
    url(r'^role/edit/(\d+)/', views.role_add_edit,name='role_edit'),
    url(r'^role/del/(\d+)/', views.role_del,name='role_del'),

    # 菜单相关
    url(r'^menu/list/', views.menu_list,name='menu_list'),
    url(r'^menu/add/', views.menu_add_edit,name='menu_add'),
    url(r'^menu/edit/(\d+)/', views.menu_add_edit,name='menu_edit'),

    #批量操作权限
    url(r'^multi/permissions/$', views.multi_permissions, name='multi_permissions'),
    # 权限分配
    url(r'^distribute/permissions/$', views.distribute_permissions, name='distribute_permissions'),

]