from django import forms
from django.core.validators import RegexValidator

from . import models


class RegisterForm(forms.Form):
    username = forms.CharField(
        # label="用户名",
        min_length=2,
        widget=forms.TextInput(attrs={'placeholder': '请输入用户名'}),
        error_messages={
            "required": "用户名不能为空！",
            "min_length": "用户名长度不能小于2个字符！",
        }

    )

    password = forms.CharField(
        # label="密码",
        min_length=6,
        widget=forms.TextInput(attrs={'type': 'password', 'placeholder': '请输入密码', 'oncontextmenu': "return false",
                                      'onpaste': "return false"}),
        error_messages={
            "required": "密码不能为空！",
            "min_length": "密码长度不能小于6位！",
        }
    )

    confirm_password = forms.CharField(
        # label="确认密码",
        widget=forms.TextInput(attrs={'type': 'password', 'placeholder': '请再次输入密码', 'oncontextmenu': "return false",
                                      'onpaste': "return false"}),
        error_messages={
            "required": "确认密码不能为空！",
        }
    )

    telephone = forms.CharField(
        # label="手机号码",
        widget=forms.TextInput(attrs={'placeholder': '手机号'}),
        validators=[RegexValidator(r'(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$', '手机号错误！')],
        error_messages={
            "required": "手机号不能为空！",
        }
    )

    email = forms.CharField(
        # label="邮箱",
        widget=forms.TextInput(attrs={'placeholder': '电子邮箱'}),
        validators=[RegexValidator(r'\w+@163.com', '邮箱格式错误！')],
        error_messages={
            "required": "邮箱不能为空！",
        }
    )

    def clean_username(self):
        user = self.cleaned_data.get("username")
        ret = models.UserInfo.objects.filter(username=user)
        if ret:
            self.add_error("username", "用户名已存在！")
        else:
            return user

    def clean(self):
        pwd = self.cleaned_data.get('password')
        cfm_pwd = self.cleaned_data.get('confirm_password')
        if pwd == cfm_pwd:
            return self.cleaned_data
        else:
            self.add_error("confirm_password", "输入密码两次不一致！")


class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={'placeholder': '请输入用户名'}),
    )

    password = forms.CharField(
        label="密码",
        widget=forms.TextInput(attrs={'type': 'password', 'placeholder': '请输入密码'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages.update({"required": "用户名不能为空！"})


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"
        exclude = ["delete_status", ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "course":
                continue
            field.widget.attrs.update({"class": "form-control"})


class ConsultRecordForm(forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        fields = "__all__"
        exclude = ["delete_status", ]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "customer":
                field.queryset = models.Customer.objects.filter(consultant__username=request.session.get("username"),
                                                                delete_status=False)
            elif name == "consultant":
                obj = models.UserInfo.objects.get(username=request.session.get("username"))
                field.choices = [(obj.id, obj.username)]
            field.widget.attrs.update({"class": "form-control"})


class CourseRecordForm(forms.ModelForm):
    class Meta:
        model = models.CourseRecord
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "has_homework":
                continue
            field.widget.attrs.update({"class": "form-control"})


class EnrollmentForm(forms.ModelForm):

    class Meta:
        model = models.Enrollment
        fields = "__all__"
        exclude = ['delete_status']

    def __init__(self,request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == "customer":
                field.queryset = models.Customer.objects.filter(consultant__username=request.session.get("username"),
                                                                delete_status=False)
            field.widget.attrs.update({"class": "form-control"})


class StudyRecordForm(forms.ModelForm):
    class Meta:
        model = models.StudyRecord
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
