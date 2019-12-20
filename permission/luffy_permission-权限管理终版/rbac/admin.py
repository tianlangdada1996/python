from django.contrib import admin
from rbac import models
# Register your models here.

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id','url','title','menu','icon']
    list_editable = ['url','title','menu','icon']
    # pass

admin.site.register(models.Menu)
admin.site.register(models.UserInfo)
admin.site.register(models.Role)
admin.site.register(models.Permission,PermissionAdmin)












