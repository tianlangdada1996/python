from django.contrib import admin

from app01.models import *
# Register your models here.

admin.site.register(UserInfo)
admin.site.register(Customer)
admin.site.register(Campuses)
admin.site.register(ClassList)
admin.site.register(ConsultRecord)
admin.site.register(Enrollment)