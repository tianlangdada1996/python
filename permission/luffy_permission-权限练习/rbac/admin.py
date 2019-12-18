from django.contrib import admin
from rbac import models


# Register your models here.

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'url', 'title', 'menu', 'icon', 'parent', 'url_name']
    list_editable = ['url', 'title', 'menu', 'icon', 'parent', 'url_name']


admin.site.register(models.FirstLevelMenu)
admin.site.register(models.UserInfo)
admin.site.register(models.Role)
admin.site.register(models.Permission,PermissionAdmin)
