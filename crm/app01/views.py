import json

from django.shortcuts import render, redirect, HttpResponse
from django.http.response import JsonResponse
from django.views import View
from django.db.models import Q
from django.conf import settings
from django.urls import reverse
from django.db import transaction
from django.forms import modelformset_factory

from . import models
from . import crmforms
from utils import encryption, paging


# Create your views here.
class Login(View):

    def get(self, request):
        login_form_obj = crmforms.LoginForm()
        return render(request, "auth/login.html", {"forms_obj": login_form_obj})

    def post(self, request):
        login_form_obj = crmforms.LoginForm(data=request.POST)
        if login_form_obj.is_valid():
            user = login_form_obj.cleaned_data["username"]
            pwd = login_form_obj.cleaned_data["password"]
            ret = models.UserInfo.objects.filter(username=user, password=encryption.encryption(user, pwd))
            if ret:
                request.session['username'] = user
                return render(request, "home.html")
            else:
                return render(request, "auth/login.html", {"forms_obj": login_form_obj, "error": "用户名密码错误！"})
        else:
            return render(request, "auth/login.html", {"forms_obj": login_form_obj})


def logout(request):
    request.session.flush()
    return redirect('app01:login')


class Register(View):

    def get(self, request):
        register_form_obj = crmforms.RegisterForm()
        return render(request, "auth/register.html", {"forms_obj": register_form_obj})

    def post(self, request):
        register_form_obj = crmforms.RegisterForm(data=request.POST)
        if register_form_obj.is_valid():
            user_data = register_form_obj.cleaned_data
            user_data.pop("confirm_password")
            user_data['password'] = encryption.encryption(user_data['username'], user_data['password'])
            models.UserInfo.objects.create(
                **user_data
            )
            return redirect("app01:login")
        else:
            return render(request, "auth/register.html", {"forms_obj": register_form_obj})


def home(request):
    return render(request, "home.html")


class Customer(View):
    res = {"status": None, "mes": None}

    def get(self, request):
        # 分页的页码每个都是一个a标签，每个标签的路径拼接上一个?page=，利用get请求获取点击的页码号，后端获取page的值即可实现逻辑处理
        current_page_num = request.GET.get("page")

        # request.get得到的是一个querydict类型，此类型源码中规定了mutable参数为False，使querydict不可改变，copy方法将此参数变为True，
        # 可以改变querydict中的参数，方便传入到封装中更新页码值
        get_data = request.GET.copy()

        # 模糊搜索中select下拉框中的选项
        action = request.GET.get("action")

        # 模糊搜索中input输入框中的模糊条件
        condition = request.GET.get("cd")

        # 筛选所有没有被假删除的人的信息
        if request.path == reverse('app01:customer'):
            tag = 1
            customers = models.Customer.objects.filter(delete_status=False, consultant__isnull=True)
        else:
            tag = 2
            customers = models.Customer.objects.filter(
                delete_status=False,
                consultant=models.UserInfo.objects.get(username=request.session.get("username")))

        # 判断有无搜索条件，如果有搜索条件利用Q查询的方法进行二次筛选
        if action and condition:
            # Q查询的第二种用法，实例化一个Q查询对象q
            q = Q()
            # 指定Q查询之间的逻辑关系or:或关系，默认为and:与关系
            q.connector = "or"
            # 利用children方法将关键字和值传入进去，每append一个列表增加一组or的关系
            # 如果action为qq__contains，condition为11，下面写法等价于 Q(qq__contains=11)
            q.children.append([action, condition])
            # 在之前筛选的基础上二次筛选，直接filter筛选q对象就能筛选出满足模糊搜索的所有对象
            customers = customers.filter(q)

        # 计算筛选出来的个数
        customer_num = customers.count()

        # 这就是封装好的分页组件，导入进来后实例化组件对象，其中的参数说明:
        # current_page_num：当前点击的页码号
        # customer_num：筛选出来客户的数量
        # get_data：GET请求的数据（copy过可以修改其中的参数）
        # settings.PAGE_NUM_SHOW：展示页码的数量，使用settings文件中配置的数量
        # settings.DATA_SHOW_NUMBER：每一页展示的数据，使用settings文件中配置的数量
        page_obj = paging.Pagination(current_page_num, customer_num, get_data, settings.PAGE_NUM_SHOW,
                                     settings.DATA_SHOW_NUMBER)

        # 调用对象的html方法拿到分页的html代码
        page_html = page_obj.html()

        # 对应分页切片模糊搜索出来的数据，使其页码与显示的数据对应上
        customers = customers[page_obj.start_data_num:page_obj.end_data_num]
        return render(request, "sales/customer_list.html",
                      {"customers": customers, "page_html": page_html, "tag": tag, "obj": models.Customer.objects})

    def post(self, request):
        cids = json.loads(request.POST.get("cids"))
        bluk_action = request.POST.get("bluk_action")

        if hasattr(self, bluk_action):
            ret = getattr(self, bluk_action)(request, cids)
            return ret
        else:
            return redirect("app01:customer")

    def transform_gs(self, request, cids):

        with transaction.atomic():
            customers = models.Customer.objects.select_for_update().filter(id__in=cids)
            msg_list = []
            for cus in customers:
                # 已经被人拿走的客户
                if cus.consultant:
                    msg_list.append(cus.name)
            msg = ','.join(msg_list) + '这几个客户已经被拿走了,回家练手速去吧!'
            models.Customer.objects.filter(id__in=cids, consultant__isnull=True).update(
                consultant=models.UserInfo.objects.get(username=request.session.get("username")))

        if msg_list:  # 选中的客户中有些客户被人拿走了
            self.res["status"] = 0
            self.res["mes"] = msg
        else:
            self.res["status"] = 1
        return JsonResponse(self.res)

    def transform_sg(self, request, cids):
        models.Customer.objects.filter(id__in=cids).update(consultant=None)
        self.res["status"] = 1
        return JsonResponse(self.res)


class CustomerAddEdit(View):

    def get(self, request, id=None):
        customer_obj = models.Customer.objects.filter(id=id)
        customer_form_obj = crmforms.CustomerForm(instance=customer_obj.first())
        return render(request, "sales/customer_addedit.html", {"fields": customer_form_obj, "cid": id})

    def post(self, request, id=None):
        next_url = request.GET.get("next")
        customer_obj = models.Customer.objects.filter(id=id)
        customer_form_obj = crmforms.CustomerForm(request.POST, instance=customer_obj.first())
        if customer_form_obj.is_valid():
            customer_form_obj.save()
            return redirect(next_url)
        else:
            return render(request, "sales/customer_addedit.html", {"fields": customer_form_obj})


def customerDel(request, id):
    next_url = request.GET.get("next")
    models.Customer.objects.filter(id=id).update(delete_status=True)
    return redirect(next_url)


class FollowRecord(View):

    def get(self, request):
        current_page_num = request.GET.get("page")
        get_data = request.GET.copy()
        action = request.GET.get("action")
        condition = request.GET.get("cd")

        cid = request.GET.get("cid")
        if cid:
            records = models.ConsultRecord.objects.filter(customer_id=cid, delete_status=False).order_by("-id")
        else:
            records = models.ConsultRecord.objects.filter(delete_status=False).order_by("-id")

        if action and condition:
            q = Q()
            q.connector = "or"
            q.children.append([action, condition])
            records = records.filter(q)
        record_num = records.count()

        page_obj = paging.Pagination(current_page_num, record_num, get_data, settings.PAGE_NUM_SHOW,
                                     settings.DATA_SHOW_NUMBER)
        page_html = page_obj.html()
        records = records[page_obj.start_data_num:page_obj.end_data_num]
        return render(request, "sales/follow_records.html",
                      {"records": records, "page_html": page_html, "obj": models.ConsultRecord.objects})

    def post(self, request):
        pass


class FollowRecordAddEdit(View):

    def get(self, request, cid=None):
        record_obj = models.ConsultRecord.objects.filter(id=cid).first()
        record_form_obj = crmforms.ConsultRecordForm(request, instance=record_obj)
        return render(request, "sales/follow_records_addedit.html", {"fields": record_form_obj, "cid": cid})

    def post(self, request, cid=None):
        next_url = request.GET.get("next")
        record_obj = models.ConsultRecord.objects.filter(id=cid).first()
        record_form_obj = crmforms.ConsultRecordForm(request, request.POST, instance=record_obj)
        if record_form_obj.is_valid():
            record_form_obj.save()
            return redirect(next_url)
        else:
            return render(request, "sales/follow_records_addedit.html", {"fields": record_form_obj, "cid": cid})


def followRecordDel(request, cid):
    next_url = request.GET.get("next")
    models.ConsultRecord.objects.filter(id=cid).update(delete_status=True)
    return redirect(next_url)


class Enrollment(View):

    def get(self, request):
        current_page_num = request.GET.get("page")
        get_data = request.GET.copy()
        action = request.GET.get("action")
        cd = request.GET.get("cd")
        enrollment_data = models.Enrollment.objects.filter(delete_status=False)

        if action and cd:
            q = Q()
            q.connector = "and"
            q.children.append([action, cd])
            enrollment_data = enrollment_data.filter(q)

        enrollment_num = enrollment_data.count()

        page_obj = paging.Pagination(current_page_num, enrollment_num, get_data, settings.PAGE_NUM_SHOW,
                                     settings.DATA_SHOW_NUMBER)
        page_html = page_obj.html()
        enrollments = enrollment_data[page_obj.start_data_num:page_obj.end_data_num]
        return render(request, "sales/enrollment_list.html", {"enrollments": enrollments, "page_html": page_html})

    def post(self, request):
        pass


class EnrollmentAddEdit(View):

    def get(self, request, cid=None):
        enrollment_obj = models.Enrollment.objects.filter(id=cid).first()
        enrollment_form_obj = crmforms.EnrollmentForm(request, instance=enrollment_obj)
        return render(request, "sales/enrollment_addedit.html", {"fields": enrollment_form_obj})

    def post(self, request, cid=None):
        next_url = request.GET.get("next")
        enrollment_obj = models.Enrollment.objects.filter(id=cid).first()
        enrollment_form_obj = crmforms.EnrollmentForm(request, request.POST, instance=enrollment_obj)
        if enrollment_form_obj.is_valid():
            enrollment_form_obj.save()
            return redirect(next_url)
        else:
            return render(request, "sales/enrollment_addedit.html", {"fields": enrollment_form_obj})


def enrollmentDel(request, cid):
    pass


class CourseRecord(View):

    def get(self, request):
        current_page_num = request.GET.get("page")
        get_data = request.GET.copy()
        action = request.GET.get("action")
        condition = request.GET.get("cd")
        records = models.CourseRecord.objects.all()
        if action and condition:
            q = Q()
            q.connector = "or"
            q.children.append([action, condition])
            records = records.filter(q)
        record_num = records.count()

        page_obj = paging.Pagination(current_page_num, record_num, get_data, settings.PAGE_NUM_SHOW,
                                     settings.DATA_SHOW_NUMBER)
        page_html = page_obj.html()
        records = records[page_obj.start_data_num:page_obj.end_data_num]
        return render(request, "sales/course_records.html",
                      {"course_records": records, "page_html": page_html, "obj": models.CourseRecord.objects})

    def post(self, request):
        bluk_action = request.POST.get("bluk_action")
        cids = json.loads(request.POST.get("cid_list"))
        if hasattr(self, bluk_action):
            ret = getattr(self, bluk_action)(request, cids)
            return ret
        else:
            return redirect(request.path)

    def bluk_create_records(self, request, cids):
        # print(cids)
        try:
            with transaction.atomic():
                for cid in cids:
                    cid = int(cid)
                    courserecord_obj = models.CourseRecord.objects.filter(id=cid).first()
                    student_objs = courserecord_obj.re_class.customer_set.filter(status="studying")
                    studyrecord_list = []
                    for student_obj in student_objs:
                        studyrecord_obj = models.StudyRecord(
                            course_record_id=cid,
                            student=student_obj
                        )
                        studyrecord_list.append(studyrecord_obj)
                    print(studyrecord_list)
                    models.StudyRecord.objects.bulk_create(studyrecord_list)
            status = 1
        except:
            status = 0
        # print(status)
        return HttpResponse(status)


class CourseRecordAddEdit(View):

    def get(self, request, cid=None):
        courserecord_obj = models.CourseRecord.objects.filter(id=cid).first()
        courserecord_form_obj = crmforms.CourseRecordForm(instance=courserecord_obj)
        return render(request, "sales/course_addedit.html", {"fields": courserecord_form_obj, "cid": cid})

    def post(self, request, cid=None):
        next_url = request.GET.get("next")
        courserecord_obj = models.CourseRecord.objects.filter(id=cid).first()
        courserecord_form_obj = crmforms.CourseRecordForm(request.POST, instance=courserecord_obj)
        if courserecord_form_obj.is_valid():
            courserecord_form_obj.save()
            return redirect(next_url)
        else:
            return render(request, "sales/course_addedit.html", {"fields": courserecord_form_obj, "cid": cid})


def courseRecordDel(request, cid):
    next_url = request.GET.get("next")
    models.CourseRecord.objects.filter(id=cid).delete()
    return redirect(next_url)


class StudyRecord(View):

    def get(self, request, cid):
        studyrecords = modelformset_factory(model=models.StudyRecord,
                                            form=crmforms.StudyRecordForm,
                                            extra=0)
        studyrecords = studyrecords(queryset=models.StudyRecord.objects.filter(course_record_id=cid))
        return render(request, "sales/study_records.html", {"study_records": studyrecords,
                                                            "obj": models.StudyRecord.objects})

    def post(self, request, cid):
        studyrecords = modelformset_factory(model=models.StudyRecord,
                                            form=crmforms.StudyRecordForm,
                                            extra=0)
        studyrecords = studyrecords(request.POST)
        if studyrecords.is_valid():
            studyrecords.save()
            return redirect("app01:course_records")
        else:
            return render(request, "sales/study_records.html", {"study_records": studyrecords,
                                                                "obj": models.StudyRecord.objects})
