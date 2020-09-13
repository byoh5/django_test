import os
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'runcoding.settings')
import django

django.setup()

from main.models import MyClassListTB
from main.models import statTB

def expire_user_class():
    year = timezone.now().year
    month = timezone.now().month
    day = timezone.now().day-1
    expire_target = MyClassListTB.objects.filter(dbstat='A', expire_time__year=year, expire_time__month=month, expire_time__day=day)
    print(expire_target.count())
    print(expire_target[0].user_id)

    for expire in expire_target:
        update_myclass = expire
        update_myclass.dbstat = 'D-' + str(year) + str(month) + str(day+1)
        update_myclass.save()

    stat_info = statTB(expire_cnt=expire_target.count())
    stat_info.save()

if __name__ == '__main__':
    expire_user_class()