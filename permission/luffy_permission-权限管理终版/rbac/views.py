from django.shortcuts import render,HttpResponse,redirect
from rbac import models
from django import forms
from django.utils.safestring import mark_safe
from rbac.serve.icons import icon_list

from rbac.serve.routes import get_all_url_dict

class RoleModelForm(forms.ModelForm):
    class Meta:
        model=models.Role
        fields = '__all__'
        exclude = ['permissions',]

        labels = {
            'role_name':'角色',
        }
        widgets = {
            'role_name':forms.TextInput(attrs={'class':'form-control'})
        }

class MenuModelForm(forms.ModelForm):
    class Meta:
        model=models.Menu
        fields = '__all__'

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'weight':forms.TextInput(attrs={'class':'form-control'}),
            'icon':forms.RadioSelect(choices=[(i[0],mark_safe(i[1])) for i in icon_list]),
        }


def role_list(request):

    role_lists = models.Role.objects.all()

    return render(request,'rbac/role_list.html',{'role_lists':role_lists})


def role_add_edit(request,rid=None):
    role_objs = models.Role.objects.filter(id=rid).first()
    if request.method == 'GET':
        form = RoleModelForm(instance=role_objs)
        return render(request, 'rbac/role_add.html', {'form': form})
    else:
        form = RoleModelForm(request.POST,instance=role_objs)
        if form.is_valid():
            form.save()
            return redirect('rbac:role_list')
        else:
            return render(request, 'rbac/role_add.html', {'form': form})


# def role_edit(request,rid):
#     role_lists = models.Role.objects.all()
#
#     return render(request, 'rbac/role_list.html', {'role_lists': role_lists})


def role_del(request,rid):
    models.Role.objects.filter(id=rid).delete()
    return redirect('rbac:role_list')


from django.db.models import Q
def menu_list(request):

    menu_lists = models.Menu.objects.all()
    # mid = request.GET.get('mid',0) #字符串类型
    mid = request.GET.get('mid') #字符串类型
    if mid:
        permissions_list = models.Permission.objects.filter(Q(menu_id=mid)|Q(parent__menu_id=mid))
    else:
        permissions_list = models.Permission.objects.all()
    return render(request,'rbac/menu_list.html',{'menu_lists':menu_lists,'permissions_list':permissions_list,'mid':mid})

def menu_add_edit(request,mid=None):
    menu_obj = models.Menu.objects.filter(id=mid).first()
    if request.method == 'GET':
        form = MenuModelForm(instance=menu_obj)
        return render(request,'rbac/menu_add.html',{'form':form})

    else:
        form = MenuModelForm(request.POST,instance=menu_obj)
        if form.is_valid():
            form.save()
            return redirect('rbac:menu_list')
        else:
            return render(request, 'rbac/menu_add.html', {'form': form})

from django.forms import modelformset_factory,formset_factory
from rbac.myform import MultiPermissionForm

def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """

    post_type = request.GET.get('type')  #add

    # 更新和编辑用的
    FormSet = modelformset_factory(models.Permission, MultiPermissionForm, extra=0)


    # 增加用的
    AddFormSet = formset_factory(MultiPermissionForm, extra=0)

    # 获取数据库中现有的所有权限数据
    permissions = models.Permission.objects.all()

    # 获取项目的路由系统中所有URL
    router_dict = get_all_url_dict(ignore_namespace_list=['admin', ])
    #{'':{'name':'','url'}}

    # 数据库中的所有权限的别名
    permissions_name_set = set([i.url_name for i in permissions])

    # 路由系统中的所有权限的别名
    router_name_set = set(router_dict.keys())



    if request.method == 'POST' and post_type == 'add':
        add_formset = AddFormSet(request.POST)
        if add_formset.is_valid():
            print(add_formset.cleaned_data)
            permission_obj_list = [models.Permission(**i) for i in add_formset.cleaned_data]

            query_list = models.Permission.objects.bulk_create(permission_obj_list)

            for i in query_list:
                permissions_name_set.add(i.url_name)

    add_name_set = router_name_set - permissions_name_set  #要新增的那些别名
    add_formset = AddFormSet(initial=[row for name, row in router_dict.items() if name in add_name_set])  #{'url_name':'','url'}
    # {'':{'name':'','url'}}

    del_name_set = permissions_name_set - router_name_set
    del_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=del_name_set))

    update_name_set = permissions_name_set & router_name_set

    update_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=update_name_set))

    if request.method == 'POST' and post_type == 'update':
        update_formset = FormSet(request.POST)
        if update_formset.is_valid():
            update_formset.save()
            update_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=update_name_set))

    return render(
        request,
        'rbac/multi_permissions.html',
        {
            'del_formset': del_formset,
            'update_formset': update_formset,
            'add_formset': add_formset,
        }
    )



def xxx(request):
    return HttpResponse('xxx')


def distribute_permissions(request):
    """
    分配权限
    :param request:
    :return:
    """

    uid = request.GET.get('uid')
    rid = request.GET.get('rid')

    if request.method == 'POST' and request.POST.get('postType') == 'role':
        user = models.UserInfo.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')  # 1  2
                                              # 1  3
        user.roles.set(request.POST.getlist('roles'))  #[2,3]

    if request.method == 'POST' and request.POST.get('postType') == 'permission' and rid:
        role = models.Role.objects.filter(id=rid).first()
        if not role:
            return HttpResponse('角色不存在')
        role.permissions.set(request.POST.getlist('permissions'))

    # 所有用户
    user_list = models.UserInfo.objects.all()
    user_has_roles = models.UserInfo.objects.filter(id=uid).values('id', 'roles')

    '''
        {}
    
    '''
    # print('xxxxxxx',user_list)
    # print(user_has_roles)

    user_has_roles_dict = {item['roles']: None for item in user_has_roles}
    # {'角色id':None,}

    """
    用户拥有的角色id
    user_has_roles_dict = { 角色id：None }
    """

    role_list = models.Role.objects.all()
    # print('rrrrr',role_list)
    if rid:
        role_has_permissions = models.Role.objects.filter(id=rid).values('id', 'permissions')
    elif uid and not rid:
        user = models.UserInfo.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        role_has_permissions = user.roles.values('id', 'permissions')

    else:
        role_has_permissions = []

    print('kkkkkk', role_has_permissions)
    '''
        <QuerySet [{'id': 4, 'permissions': 1}, {'id': 4, 'permissions': 2}, {'id': 4, 'permissions': 3}, {'id': 4, 'permissions': 4}, {'id': 4, 'permissions': 5}, {'id': 4, 'permissions': 6}, {'id': 4, 'permissions': 7}, {'id': 4, 'permissions': 8}, {'id': 4, 'permissions': 9}, {'id': 4, 'permissions': 10}, {'id': 4, 'permissions': 11}, {'id': 4, 'permissions': 12}, {'id': 4, 'permissions': 13}, {'id': 4, 'permissions': 14}, {'id': 4, 'permissions': 15}, {'id': 4, 'permissions': 16}]>
    
    '''
    role_has_permissions_dict = {item['permissions']: None for item in role_has_permissions}

    '''
        {1:None,2:None}
        if 3 in {1:None,2:None}
    '''


    """
    角色拥有的权限id
    role_has_permissions_dict = { 权限id：None }
    """

    all_menu_list = []
    '''
        [
            {'id':1,'title':'业务管理','children':[
                
                {'id':1,title:'客户展示','menu_id':1,'children':[
                    {'id':2,'title':'客户添加','parent_id':1}
                ]}
            
            ]},
            {'id':2,'title':'财务管理','children':[
                {'id':5,title:'缴费展示','menu_id':2,'children':[]}
            ]},
            {'id': None, 'title': '其他', 'children': [
                {'id':9,'title':'嘻嘻嘻',parent_id:None}
            ]}
        ]
        
    '''

    queryset = models.Menu.objects.values('id', 'title')
    '''
        queryset<[{'id':1,'title':'业务管理','children':[]},]>
    '''
    menu_dict = {}
    '''
        {
            1:{'id':1,'title':'业务管理','children':[
            
                {'id':1,title:'客户展示','menu_id':1,'children':[]}
            ]},
            2:{'id':2,'title':'财务管理','children':[
                {'id':5,title:'缴费展示','menu_id':2,'children':[]}
            ]},
            None:{'id': None, 'title': '其他', 'children': [
                {'id':9,'title':'嘻嘻嘻',parent_id:None}
            ]},
        }
    '''

    for item in queryset:
        item['children'] = []  # 放二级菜单，父权限
        menu_dict[item['id']] = item
        all_menu_list.append(item)

    other = {'id': None, 'title': '其他', 'children': []}
    all_menu_list.append(other)
    menu_dict[None] = other

    root_permission = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id') #二级菜单权限
    '''
        queryset<[{'id':1,title:'客户展示','menu_id':1,'children':[]},]>
    '''
    root_permission_dict = {}
    '''
        {
            二级菜单权限id
            1:{'id':1,title:'客户展示','menu_id':1,'children':[
                {'id':2,'title':'客户添加','parent_id':1}
            ]},
            5:{'id':5,title:'缴费展示','menu_id':2,'children':[]},
        }
    '''

    for per in root_permission:
        per['children'] = []  # 放子权限
        nid = per['id']  #二级菜单权限id
        menu_id = per['menu_id']  # 一级菜单权限id
        root_permission_dict[nid] = per
        menu_dict[menu_id]['children'].append(per)

    node_permission = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'parent_id') #二级菜单子权限
    '''
        queryset<[{'id':2,'title':'客户添加','parent_id':1},{'id':9,'title':'嘻嘻嘻',parent_id:None}]>
    '''
    for per in node_permission:
        pid = per['parent_id']
        if not pid:
            menu_dict[None]['children'].append(per)
            continue
        root_permission_dict[pid]['children'].append(per)

    return render(
        request,
        'rbac/distribute_permissions.html',
        {
            'user_list': user_list,
            'role_list': role_list,
            'user_has_roles_dict': user_has_roles_dict,
            'role_has_permissions_dict': role_has_permissions_dict,
            'all_menu_list': all_menu_list,
            'uid': uid,
            'rid': rid
        }
    )













