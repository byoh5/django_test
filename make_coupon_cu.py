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

    period = 12 * 30
    expireTime = timezone.now() + timezone.timedelta(days=period)

    add_coupon = couponTB(coupon_num=coupon_num, coupon_name=coupon_name, coupon_type=200,
                                         prd=prd[0], period=12, expire=expireTime, dbstat='A')
    add_coupon.save()

    print(coupon_num, coupon_name, prd_code[0].title)

def make():
    coupon_num_as = 'cuas'
    coupon_num_ms = 'cums'
    coupon_num_an = 'cuan'
    coupon_num_mn = 'cumn'

    for i in range(50):
        print(coupon_num_as, i)
        add_coupon(coupon_num_as, "스마트 휴지통(+AI) 아두이노 버전", "2020080013001")

    for i in range(50):
        print(coupon_num_ms, i)
        add_coupon(coupon_num_ms, "스마트 휴지통(+AI) 엠블럭 버전", "2020080023001")

    for i in range(50):
        print(coupon_num_an, i)
        add_coupon(coupon_num_an, "네오픽셀 아두이노 버전", "2020120030002")

    for i in range(50):
        print(coupon_num_mn, i)
        add_coupon(coupon_num_mn, "네오픽셀 엠블럭 버전", "2020120040002")

if __name__ == '__main__':
    make()