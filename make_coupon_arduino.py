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
    # naming [arduino, make, kit]
    coupon_num_arduino_smart = 'asm_' #asm_, amsm_
    coupon_num_arduino_smart_make = 'amsm_'  # asm_, amsm_
    coupon_num_arduino_ai_trashcan = 'amait_' #asm_, amsm_
    coupon_num_arduino_neopixel = 'ane_'
    coupon_num_arduino_ai_charm = 'amaic_'

    # for i in range(36):
    #     print(coupon_num_arduino_smart_make, i)
    #     add_coupon(coupon_num_arduino_smart_make, "스마트 휴지통 아두이노 maker", "202008am_smart") #202008am_smart , 202008a_smart

    # for i in range(36):
    #     print(coupon_num_arduino_ai_trashcan, i)
    #     add_coupon(coupon_num_arduino_ai_trashcan, "인공지능 휴지통 아두이노 maker", "202008am_aiTrashcan") #	202008am_aiTrashcan

    for i in range(36):
        print(coupon_num_arduino_neopixel, i)
        add_coupon(coupon_num_arduino_neopixel, "네오픽셀 아두이노 버전", "202012a_neopixel") #202012am_neopixel

    # for i in range(36):
    #     print(coupon_num_arduino_ai_charm, i)
    #     add_coupon(coupon_num_arduino_ai_charm, "참참참 인공지능 아두이노 maker", "202108am_aiCharm") #202108am_aiCharm

    # for i in range(36):
    #     print(coupon_num_arduino_smart, i)
    #     add_coupon(coupon_num_arduino_smart, "스마트 휴지통 아두이노 버전", "202008a_smart") #202008am_smart , 202008a_smart


if __name__ == '__main__':
    make()