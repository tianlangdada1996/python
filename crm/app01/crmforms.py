from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from . import models
from crmtools import encryption


class Register(forms.Form):
    username = forms.CharField(
        label="用户名",
        min_length=2,
        widget=forms.TextInput(attrs={'placeholder': '请输入用户名'}),
        error_messages={
            "required": "用户名不能为空！",
            "min_length": "用户名长度不能小于2个字符！",
        }

    )

    password = forms.CharField(
        label="密码",
        min_length=6,
        widget=forms.TextInput(attrs={'type': 'password', 'placeholder': '请输入密码'}),
        error_messages={
            "required": "密码不能为空！",
            "min_length": "密码长度不能小于6位！",
        }
    )

    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.TextInput(attrs={'type': 'password', 'placeholder': '请再次输入密码'}),
        error_messages={
            "required": "确认密码不能为空！",
        }
    )

    telephone = forms.CharField(
        label="手机号码",
        widget=forms.TextInput(attrs={'placeholder': '手机号'}),
        validators=[RegexValidator(r'(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$', '手机号错误！')],
        error_messages={
            "required": "手机号能为空！",
        }
    )

    email = forms.CharField(
        label="邮箱",
        widget=forms.TextInput(attrs={'placeholder': '电子邮箱'}),
        validators=[RegexValidator(r'\w+@163.com', '邮箱格式错误！')],
        error_messages={
            "required": "邮箱不能为空！",
        }
    )

    def clean_username(self):
        user = self.cleaned_data.get("username")
        ret = models.UserInfo.objects.filter(username=user).first()
        if ret:
            raise ValidationError("用户名已存在！")
        else:
            return user

    def clean(self):
        pwd = self.cleaned_data.get('password')
        cfm_pwd = self.cleaned_data.get('confirm_password')
        if pwd == cfm_pwd:
            return self.cleaned_data
        else:
            self.add_error("confirm_password", "输入密码两次不一致！")


class Login(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={'placeholder': '请输入用户名'}),
        error_messages={
            "required": "用户名不能为空！",
        }
    )

    password = forms.CharField(
        label="密码",
        widget=forms.TextInput(attrs={'type': 'password', 'placeholder': '请输入密码'}),
        error_messages={
            "required": "密码不能为空！",
        }
    )

    def clean(self):
        user = self.cleaned_data.get("username")
        pwd = self.cleaned_data.get("password")
        en_pwd = encryption.encryption(user, pwd)
        ret = models.UserInfo.objects.filter(username=user, password=en_pwd).first()
        if ret:
            return self.cleaned_data
        else:
            self.add_error("password", "用户名密码错误！")
