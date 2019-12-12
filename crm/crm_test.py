import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

    import django
    django.setup()

    from app01 import models
    # print(models.UserInfo.objects.filter(id=1).values("is_active"))

    # obj_list = []
    # for i in range(500):
    #     obj = models.Customer(
    #         qq=f"{i}{i}{i}",
    #         name=f"yzm{i}",
    #         course=['PythonFullStack'],
    #     )
    #     obj_list.append(obj)
    # models.Customer.objects.bulk_create(obj_list)
    models.Customer.objects.filter(name__contains="yzm").update(sex="female")