import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

    import django
    django.setup()

    # from app01 import models
    # print(models.UserInfo.objects.filter(id=1).values("is_active"))
