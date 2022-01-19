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
    # make class
    # naming [entry, make, kit]

    coupon_num_entry_ai_charm = 'emaic_'
    coupon_num_entry_smart = 'emsm_'
    coupon_num_entry_smart_make = 'emsm_'
    coupon_num_entry_music_make = 'emmu_'
    coupon_num_entry_music = 'emu_'
    coupon_num_entry_save_make = 'emsa_'
    coupon_num_entry_save = 'esa_'
    coupon_num_entry_bright_make = 'embr_'
    coupon_num_entry_neopixel = 'ene_'
    coupon_num_entry_neopixel_make = 'enem_'

    # for i in range(36):
    #     print(coupon_num_entry_ai_charm, i)
    #     add_coupon(coupon_num_entry_ai_charm, "인공지능 참참참 엔트리 maker", "202104em_aiCharm")

    # for i in range(36):
    #     print(coupon_num_entry_smart_make, i)
    #     add_coupon(coupon_num_entry_smart_make, "스마트 휴지통 엔트리 maker", "202106em_smart")

    # for i in range(36):
    #     print(coupon_num_entry_smart, i)
    #     add_coupon(coupon_num_entry_smart, "스마트 휴지통 엔트리", "202106e_smart")

    # for i in range(36):
    #     print(coupon_num_entry_music_make, i)
    #     add_coupon(coupon_num_entry_music_make, "뮤직박스 엔트리 maker", "202108em_musicbox")

    # for i in range(36):
    #     print(coupon_num_entry_music, i)
    #     add_coupon(coupon_num_entry_music, "뮤직박스 엔트리 버전", "202108e_musicbox")

    # for i in range(36):
    #     print(coupon_num_entry_save_make, i)
    #     add_coupon(coupon_num_entry_save_make, "저금통 엔트리 maker", "202111em_savebot")


    # for i in range(36):
    #     print(coupon_num_entry_save, i)
    #     add_coupon(coupon_num_entry_save, "저금통 엔트리 버전", "202111e_savebot")

    # for i in range(36):
    #     print(coupon_num_entry_bright_make, i)
    #     add_coupon(coupon_num_entry_bright_make, "반짝반짝 LED 액자 엔트리 버전", "202112em_bright")

    for i in range(36):
        print(coupon_num_entry_neopixel, i)
        add_coupon(coupon_num_entry_neopixel, "반짝반짝 똥머리한 네오픽셀", "202111e_neopixel")


if __name__ == '__main__':
    make()