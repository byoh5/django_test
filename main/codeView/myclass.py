from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from main.query import *
from main.models import *
from main.codeView.stat import stat_menu_step
message_no_login = 210

def myclass_list_page(request):
    user_id = request.session.get('user_id')
    session = request.session.get('client_id')
    stat_menu_step(request, "myclass_list", "", "")
    if user_id is not None:
        if checkSession(session, user_id):
            myclass_list_info = select_myclass_list(user_id)

            context = {
                "myclass_list_detail": myclass_list_info,
                "count": myclass_list_info.count(),
            }
            return render(request, 'myclass/myclass_list.html', context)
        else:
            disableSession(user_id, request)
            return render(request, 'login/login.html')
    else:
        return render(request, 'login/login.html')

def Bonus_page(request):
    prdCode = request.POST.get('prdCode', '')
    if prdCode == '':
        return myclass_list_page(request)

    itemCode = request.POST['itemCode']

    myclass_idx = request.POST['myclass_idx']
    play = request.POST['myclass_play']
    user_id = request.session.get('user_id')
    session = request.session.get('client_id')

    stat_menu_step(request, "myclass_list", "BonusClass", prdCode + "||" + itemCode)

    if user_id is not None:
        if checkSession(session, user_id):
            item_Bonus_info = select_class_item_Bonus(prdCode, itemCode)

            print(prdCode, itemCode)
            print(item_Bonus_info.count())

            print(item_Bonus_info[0].iteminfo_2.downdata_name)

            if item_Bonus_info.count() > 0:
                context = {
                    "Bonus_list": item_Bonus_info,
                    "data" : item_Bonus_info[0].data,
                    "title": item_Bonus_info[0].title,
                    "subTitle": item_Bonus_info[0].subTitle,
                    "myclass_idx": myclass_idx,
                    "play": play,
                }
                return render(request, 'myclass/myclass_Bonus.html', context)
        else:
            disableSession(user_id, request)
            return render(request, 'login/login.html')
    else:
        return render(request, 'login/login.html')


def myclass_page(request):
    prdCode = request.POST.get('prdCode', '')
    if prdCode == '':
       return myclass_list_page(request)

    print(prdCode)

    bonus_code = prdCode.split('_')

    print(bonus_code)

    if bonus_code[0] == 'bonus':
        return Bonus_page(request)

    itemCode = request.POST['itemCode']

    myclass_idx = request.POST['myclass_idx']
    play = request.POST['myclass_play']
    user_id = request.session.get('user_id')
    session = request.session.get('client_id')

    stat_menu_step(request, "myclass_list", "myclass", prdCode + "||" + itemCode)

    if user_id is not None:
        if checkSession(session, user_id):
            item_info = select_class_item_detail(prdCode, itemCode)
            item_common_info = select_class_item_common_detail(prdCode, itemCode)
            item_sub_info = select_class_item_sub_detail(prdCode, itemCode)

            if item_info.count() > 0:
                context = {
                    "myclass_detail": item_info,
                    "myclass_common_detail": item_common_info,
                    "myclass_sub_detail": item_sub_info,
                    "title": item_info[0].item_code,
                    "subTitle": item_info[0].prd.keyword,
                    "myclass_idx":myclass_idx,
                    "play":play,
                }
                return render(request, 'myclass/myclass.html', context)
        else:
            disableSession(user_id, request)
            return render(request, 'login/login.html')
    else:
        return render(request, 'login/login.html')

def video_play_page(request):
    myclass_idx = request.POST['myclass_idx']
    data = request.POST['data']

    myclass_list_info = select_myclass_list_play(myclass_idx)

    if myclass_list_info.count() > 0:
        stat_class_info = stat_class(pay_email=myclass_list_info[0].user_id, myclass=myclass_list_info[0],
                                     prd_code=myclass_list_info[0].prd.prd_code, item_code=myclass_list_info[0].item_code,
                                     class_title=myclass_list_info[0].prd.title, class_data=data)
        stat_class_info.save()

        year = timezone.localtime().year
        month = timezone.localtime().month
        day = timezone.localtime().day

        if myclass_list_info[0].play == 'D':
            new_myclass = myclass_list_info[0]
            new_myclass.play = 'A'
            new_myclass.play_time = str(year) + "-" + str(month) + "-" + str(day)
            new_myclass.play_video = data
            new_myclass.save()

    return HttpResponse(200)
