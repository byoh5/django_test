import os
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'runcoding.settings')
import django

django.setup()

from main.models import couponTB

def expire_coupon():
    year = timezone.localtime().year
    month = timezone.localtime().month
    day = timezone.localtime().day-1
    expire_target = couponTB.objects.filter(dbstat='A', expire__year=year, expire__month=month, expire__day=day)

    if expire_target.count() != 0:
        for expire in expire_target:
            update_coupon = expire
            update_coupon.dbstat = 'D-' + str(year) + str(month) + str(day+1)
            update_coupon.save()

        print("expire target is ", expire_target.count(), " (data : ", year, month, day, ")")
    else:
        print("expire target is 0 (data : ",year, month, day ,")")

if __name__ == '__main__':
    expire_coupon()