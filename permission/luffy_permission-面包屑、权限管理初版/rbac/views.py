from django.shortcuts import render,HttpResponse,redirect
from rbac import models
from django import forms
from django.utils.safestring import mark_safe
from rbac.serve.icons import icon_list

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
            return redirect('role_list')
        else:
            return render(request, 'rbac/role_add.html', {'form': form})


# def role_edit(request,rid):
#     role_lists = models.Role.objects.all()
#
#     return render(request, 'rbac/role_list.html', {'role_lists': role_lists})


def role_del(request,rid):
    models.Role.objects.filter(id=rid).delete()
    return redirect('role_list')


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
            return redirect('menu_list')
        else:
            return render(request, 'rbac/menu_add.html', {'form': form})
