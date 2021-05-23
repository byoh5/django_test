import os
import string

from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'runcoding.settings')
import django
import random
django.setup()

from main.models import couponTB
from main.models import PrdTB

#cuas
#cums
#cuan
#cumn

def add_coupon(coupon_num, coupon_name, prd_code):
    prd = PrdTB.objects.filter(prd_code=prd_code, dbstat='A')

    number_pool = string.digits
    _LENGTH = 12
    for i in range(_LENGTH):
        coupon_num += random.choice(number_pool)  # 랜덤한 문자열 하나 선택

    period = 12 * 3
    expireTime = timezone.now() + timezone.timedelta(days=period)

    add_coupon = couponTB(coupon_num=coupon_num, coupon_name=coupon_name, coupon_type=200,
                                         prd=prd[0], period=12, expire=expireTime, dbstat='A')
    add_coupon.save()

    print(coupon_num, coupon_name, prd_code[0].title)

def make():
    coupon_num_entry_ai_charm = 'enaic_'

    for i in range(30):
        print(coupon_num_entry_ai_charm, i)
        add_coupon(coupon_num_entry_ai_charm, "참참참 인공지능 게임 엔트리 버전", "2021040053003") #	2021040053003


if __name__ == '__main__':
    make()