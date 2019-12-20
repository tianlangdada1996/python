from django.shortcuts import render, redirect
from django.views import View
from django import forms

from rbac import models


class RoleForm(forms.ModelForm):
    class Meta:
        model = models.Role
        fields = ["role_name"]
        labels = {
            "role_name": "角色"
        }
        widgets = {
            "role_name": forms.TextInput(attrs={'class': 'form-control'})
        }


# Create your views here.
def rolelist(request):
    role_lists = models.Role.objects.all()
    return render(request, "role_list.html", {"role_lists": role_lists})


class RoleAddEdit(View):

    def get(self, request, rid=None):
        role_obj = models.Role.objects.filter(id=rid).first()
        roleform = RoleForm(instance=role_obj)
        return render(request, "role_addedit.html", {"form": roleform})

    def post(self, request, rid=None):
        role_obj = models.Role.objects.filter(id=rid).first()
        roleform = RoleForm(request.POST, instance=role_obj)
        if roleform.is_valid():
            roleform.save()
            return redirect("rbac:role_list")
        else:
            return render(request, "role_addedit.html", {"form": roleform})


def roledel(request, rid):
    models.Role.objects.filter(id=rid).delete()
    return redirect("rbac:role_list")


class MenuList(View):

    def get(self, request):
        return render(request, "menu_list.html")
