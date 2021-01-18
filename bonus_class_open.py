import os
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'runcoding.settings')
import django
django.setup()

from main.models import MyClassListTB
from main.models import BonusItemTB
from main.models import bonus_prd

def myclassList(user_id, prd_code, item_code):
    myclass_list_info = MyClassListTB.objects.filter(user_id=user_id, bonus__bonus_prdCode=prd_code,
                                                     item_code=item_code, dbstat='A')
    return myclass_list_info

def bonus_class():
    bonus_info = bonus_prd.objects.filter(cron='A', dbstat='A') #bonus active가 존재하면

    print(bonus_info.count())
    for bonus in bonus_info:
        bonus_prd_code = bonus.bonus_prdCode  #등록된 보너스 prd_code
        myclass_target1_prd = MyClassListTB.objects.filter(prd__prd_code=bonus.targetPrd_1.prd_code, dbstat='A') #대상이 되는 prd를 구매한 list
        myclass_target2_prd = MyClassListTB.objects.filter(prd__prd_code=bonus.targetPrd_2.prd_code, dbstat='A') # 대상이 되는 prd를 구매한 list
        item_info = BonusItemTB.objects.filter(prd__bonus_prdCode=bonus_prd_code, dbstat='A')  # 보너스 클래스 item

        print(bonus_prd_code)
        print(item_info[0].item_code)

        print(myclass_target1_prd.count())
        print(myclass_target2_prd.count())

        for myclass_target1 in myclass_target1_prd:

            myclass_bonus = myclassList(myclass_target1.user_id, bonus_prd_code, item_info[0].item_code) #존재하는 동일한 보너스가 있는지

            if myclass_bonus.count() == 0: #동일한 보너스가 없다면
                period = bonus.period * 30
                expireTime = timezone.now() + timezone.timedelta(days=period)
                year = timezone.localtime().year
                month = timezone.localtime().month
                day = timezone.localtime().day
                play_time = str(year) + "-" + str(month) + "-" + str(day)
                myclass_list_info = MyClassListTB(user_id=myclass_target1.user_id, bonus=bonus,
                                                  pay_num='bonus_class', item_code=item_info[0].item_code,
                                                  play_time=play_time,
                                                  play='A', expire_time=expireTime)
                myclass_list_info.save()

        for myclass_target2 in myclass_target2_prd:
            myclass_bonus2 = myclassList(myclass_target2.user_id, bonus_prd_code,
                                                      item_info[0].item_code)  # 존재하는 동일한 보너스가 있는지

            if myclass_bonus2.count() == 0:  # 동일한 보너스가 없다면
                period = bonus.period * 30
                expireTime = timezone.now() + timezone.timedelta(days=period)
                year = timezone.localtime().year
                month = timezone.localtime().month
                day = timezone.localtime().day
                play_time = str(year) + "-" + str(month) + "-" + str(day)
                myclass_list_info = MyClassListTB(user_id=myclass_target2.user_id, bonus=bonus,
                                                  pay_num='bonus_class', item_code=item_info[0].item_code,
                                                  play_time=play_time,
                                                  play='A', expire_time=expireTime)
                myclass_list_info.save()

    new_bonus = bonus_info[0]
    new_bonus.cron = 'D'
    new_bonus.save()

if __name__ == '__main__':
    bonus_class()