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
    url(r'^records/follow/edit/(\d+)/$', views.FollowRecordAddEdit.as_view(), name='follow_records_edit'),
    url(r'^records/follow/del/(\d+)/$', views.followRecordDel, name='follow_records_del'),
    url(r'^enrollment/$', views.Enrollment.as_view(), name='enrollment'),
    url(r'^enrollment/add/$', views.EnrollmentAddEdit.as_view(), name='enrollment_add'),
    url(r'^enrollment/edit/(\d+)/$', views.EnrollmentAddEdit.as_view(), name='enrollment_edit'),
    url(r'^enrollment/del/(\d+)/$', views.enrollmentDel, name='enrollment_del'),
    url(r'^records/course/$', views.CourseRecord.as_view(), name='course_records'),
    url(r'^records/course/add/$', views.CourseRecordAddEdit.as_view(), name='course_records_add'),
    url(r'^records/course/edit/(\d+)/$', views.CourseRecordAddEdit.as_view(), name='course_records_edit'),
    url(r'^records/course/del/(\d+)/$', views.courseRecordDel, name='course_records_del'),
    url(r'^records/study/(\d+)/$', views.StudyRecord.as_view(), name='study_records'),
]
