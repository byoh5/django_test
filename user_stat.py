import os
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'runcoding.settings')
import django

django.setup()

from main.models import RegisterTB
from main.models import LoginTB
from main.models import PayTB
from main.models import statTB

def user_stat():
    year = timezone.localtime().year
    month = timezone.localtime().month
    day = timezone.localtime().day-1
    register_cnt = RegisterTB.objects.filter(dbstat='A', stime__year=year, stime__month=month, stime__day=day).count()
    login_cnt = LoginTB.objects.filter(dbstat='A', login_time__year=year, login_time__month=month, login_time__day=day).count()
    pay_suc_cnt = PayTB.objects.filter(pay_time__year=year, pay_time__month=month, pay_time__day=day, pay_result=0).count()
    pay_fail_cnt = PayTB.objects.filter(pay_time__year=year, pay_time__month=month, pay_time__day=day, pay_result=1).count()
    pre_pay_cnt = PayTB.objects.filter(pay_time__year=year, pay_time__month=month, pay_time__day=day, pay_result=100).count()

    stat_info = statTB.objects.filter(stime__year=year, stime__month=month, stime__day=day+1)

    if stat_info.count() == 1:
        new_stat = stat_info[0]
        new_stat.register_cnt = register_cnt
        new_stat.login_cnt = login_cnt
        new_stat.pay_suc_cnt = pay_suc_cnt
        new_stat.pay_fail_cnt = pay_fail_cnt
        new_stat.pre_pay_cnt = pre_pay_cnt
        new_stat.save()
    else:
        stat_info = statTB(register_cnt=register_cnt, login_cnt=login_cnt, pay_suc_cnt=pay_suc_cnt, pay_fail_cnt=pay_fail_cnt, pre_pay_cnt=pre_pay_cnt)
        stat_info.save()

if __name__ == '__main__':
    user_stat()