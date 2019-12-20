from django.db import models

# Create your models here.

class Menu(models.Model):
    """
    一级菜单表
    """
    title = models.CharField(max_length=32,verbose_name='菜单名称')  #财务管理
    weight = models.IntegerField(default=100,verbose_name='权重')
    icon = models.CharField(max_length=32, null=True, blank=True, verbose_name='图标')
    def __str__(self):
        return self.title

class UserInfo(models.Model):

    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    roles = models.ManyToManyField('Role')

    def __str__(self):
        return self.username

class Role(models.Model):

    role_name = models.CharField(max_length=16)
    permissions = models.ManyToManyField('Permission')

    def __str__(self):
        return self.role_name

class Permission(models.Model):

    url = models.CharField(max_length=1200)  #/customers/
    title = models.CharField(max_length=32)  # 客户展示
    # is_menu = models.BooleanField(default=False)  #通过这个字段判断这条权限是否是左侧菜单权限
    menu = models.ForeignKey('Menu',null=True,blank=True)  #
    parent = models.ForeignKey('self',null=True,blank=True)
    url_name = models.CharField(max_length=32,null=True,blank=True)
    icon = models.CharField(max_length=32,null=True,blank=True)  #菜单图标


    def __str__(self):
        return self.title












