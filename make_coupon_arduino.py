import os
import string

from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'runcoding.settings')
import django
import random
django.setup()

from main.models import couponTB
from main.models import PrdTB


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
    coupon_num_arduino_smart = 'asm_'
    coupon_num_arduino_ai_trashcan = 'aait_'
    coupon_num_arduino_neopixel = 'aneo_'

    for i in range(5):
        print(coupon_num_arduino_smart, i)
        add_coupon(coupon_num_arduino_smart, "스마트 휴지통 아두이노 버전", "2020080013001") #2020080013001

    for i in range(5):
        print(coupon_num_arduino_ai_trashcan, i)
        add_coupon(coupon_num_arduino_ai_trashcan, "인공지능 휴지통 아두이노 버전", "2020080013002") #	2020080013002

    for i in range(5):
        print(coupon_num_arduino_neopixel, i)
        add_coupon(coupon_num_arduino_neopixel, "네오픽셀 아두이노 버전", "2020120030002") #2020120030002


if __name__ == '__main__':
    make()