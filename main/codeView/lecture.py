from django.shortcuts import render
from django.utils import timezone

from main.query import *
from main.codeView.stat import stat_menu_step
from main.codeView.main import *

imp_id = 'imp08800373'

def class_page(request):
    class_list_info = select_class_list()
    category_large = select_class_category_lar_list()

    stat_menu_step(request,"codingkit_list", "", "")

    context = {
        "class_list_detail": class_list_info,
        "category_large": category_large,
        "total_count": class_list_info.count(),
    }

    return render(request, 'class/class_list.html', context)

def class_detail_page(request):
    user_id = request.session.get('user_id', '')
    if user_id == '':
        user = "n"
    else:
        user = "y"

    prd_code = request.POST.get('detail_prd_code', 0)
    # items_info = select_class_detail(prd_code)

    if prd_code == 0:
        return class_page(request)

    prd_info = select_prd(prd_code)
    print(prd_code)
    html_file = ""

    html_file = "product/" + prd_info[0].list + ".html"

    stat_menu_step(request, "codingkit_detail", prd_info[0].title + "(" + prd_code + ") ||" + html_file, "")

    context = {
        "prd_detail": prd_info[0],
        "html_file": html_file,
    }

    return render(request, 'class/class_detail.html', context)


def class_detail_page_prd(request):
    prd_code = request.GET.get('prd_code')
    context = {
        "prd_code": prd_code,
    }

    return render(request, 'class/class_store_detail.html', context)

#구매시점에 bonus prd가 있으면 생성
def bonus_class(user_id, prd_code, pay_num, dbstat):
    bonus_target = select_bonus_prd(prd_code) # 내가 구매한 prd에 bonus 가 있는지 확인

    print(prd_code)
    print(bonus_target.count() )

    if bonus_target.count() > 0:
        bonus_prdCode = bonus_target[0].bonus_prdCode
        item_info = select_bonus_item(bonus_prdCode) # 보너스 prd의 item
        myclass_bonus = select_myclass_list_bonus(user_id, bonus_prdCode, item_info[0].item_code) # 내강의실에 같은 보너스가 있는지 확인

        print(user_id, bonus_prdCode, item_info[0].item_code)
        print(myclass_bonus.count())

        if myclass_bonus.count() == 0:
            period = item_info[0].prd.period * 30
            expireTime = timezone.now() + timezone.timedelta(days=period)
            year = timezone.localtime().year
            month = timezone.localtime().month
            day = timezone.localtime().day
            play_time = str(year) + "-" + str(month) + "-" + str(day)
            myclass_list_info = MyClassListTB(user_id=user_id, bonus=item_info[0].prd,
                                              pay_num=pay_num, item_code=item_info[0].item_code, play_time=play_time,
                                              play='A', expire_time=expireTime, dbstat=dbstat)
            myclass_list_info.save()


