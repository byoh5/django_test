import os
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'runcoding.settings')
import django

django.setup()

from main.models import MyClassListTB
from main.models import statTB

def expire_user_class():
    year = timezone.localtime().year
    month = timezone.localtime().month
    day = timezone.localtime().day-1
    expire_target = MyClassListTB.objects.filter(dbstat='A', expire_time__year=year, expire_time__month=month, expire_time__day=day)

    if expire_target.count() != 0:
        for expire in expire_target:
            update_myclass = expire
            update_myclass.dbstat = 'D-' + str(year) + str(month) + str(day+1)
            update_myclass.save()

        print("expire target is ", expire_target.count(), " (data : ", year, month, day, ")")
    else:
        print("expire target is 0 (data : ",year, month, day ,")")

    stat_info = statTB(expire_cnt=expire_target.count())
    stat_info.save()

if __name__ == '__main__':
    expire_user_class()