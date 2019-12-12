from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^home/$', views.home, name='home'),
    url(r'^customer/$', views.Customer.as_view(), name='customer'),
    url(r'^mycustomer/$', views.Customer.as_view(), name='mycustomer'),
    url(r'^customer/add/$', views.CustomerAddEdit.as_view(), name='customer_add'),
    url(r'^customer/edit/(\d+)/$', views.CustomerAddEdit.as_view(), name='customer_edit'),
    url(r'^customer/del/(\d+)/$', views.customerDel, name='customer_del'),
    url(r'^records/follow/$', views.FollowRecord.as_view(), name='follow_records'),
    url(r'^records/follow/add/$', views.FollowRecordAddEdit.as_view(), name='follow_records_add'),
    url(r'^records/follow/edit/(\d+)$', views.FollowRecordAddEdit.as_view(), name='follow_records_edit'),
    url(r'^records/follow/del/(\d+)$', views.followRecordDel, name='follow_records_del')
]
