from django import template
from django.conf import settings
from django.urls import reverse
from django.http.request import QueryDict

from app01 import models

register = template.Library()


@register.simple_tag
def list_number(request, forloop_counter, models_obj):
    try:
        page_number = int(request.GET.get("page"))
        models_num = models_obj.count()
        a, b = divmod(models_num, settings.DATA_SHOW_NUMBER)
        page_total = a + 1 if b else a
        if page_number < 1:
            page_number = 1
        elif page_number > page_total:
            page_number = page_total
    except Exception:
        page_number = 1
    return (page_number - 1) * settings.DATA_SHOW_NUMBER + forloop_counter


@register.filter
def title_name(url):
    if url == reverse("app01:customer"):
        return "公户信息"
    else:
        return "我的客户"


@register.simple_tag
def resolve_url(request, url, cid=None, data_count=None):
    custom = QueryDict(mutable=True)
    if cid:
        get_data = request.GET.copy()
        if data_count == 1 and get_data.get("page"):
            get_data["page"] = int(get_data.get("page")) - 1
        elif data_count == 1 and not get_data.get("page"):
            get_data["page"] = 1
        reverse_url = reverse(url, args=(cid,))
        custom["next"] = request.path + "?" + get_data.urlencode()
    else:
        reverse_url = reverse(url)
        custom["next"] = request.get_full_path()

    next_path = custom.urlencode()
    return reverse_url + "?" + next_path
