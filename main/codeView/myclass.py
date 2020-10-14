from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from main.query import *
from main.models import *

message_no_login = 210

def myclass_list_page(request):
    user_id = request.session.get('user_id')
    session = request.session.get('client_id')
    if user_id is not None:
        if checkSession(session, user_id):
            myclass_list_info = select_myclass_list(user_id)

            context = {
                "myclass_list_detail": myclass_list_info,
            }
            return render(request, 'myclass/myclass_list.html', context)
        else:
            return render(request, 'myclass/myclass_list.html')

        return render(request, 'myclass/myclass_list.html')
    else:
        return render(request, 'login/login.html')


def myclass_page(request):
    prdCode = request.POST['prdCode']
    myclass_idx = request.POST['myclass_idx']
    play = request.POST['myclass_play']
    user_id = request.session.get('user_id')
    session = request.session.get('client_id')

    if checkSession(session, user_id):
        item_info = select_class_kit_detail(prdCode)
        item_common_info = select_class_common_detail(prdCode)

        if item_info.count() > 0:
            context = {
                "myclass_detail": item_info,
                "myclass_common_detail": item_common_info,
                "title": item_info[0].prd.title2,
                "sub_title": item_info[0].prd.title3,
                "myclass_idx":myclass_idx,
                "play":play,
            }
            return render(request, 'myclass/myclass.html', context)

        else:
            return render(request, 'myclass/myclass_list.html')
    else:
        disableSession(user_id, request)
        context = {
            "msg": message_no_login,
        }
        return render(request, 'login/login.html', context)

def video_play_page(request):
    myclass_idx = request.POST['myclass_idx']
    prdCode = request.POST['prdCode']
    data = request.POST['data']

    myclass_list_info = select_myclass_list_play(myclass_idx)

    time = timezone.localtime()

    year = time.year
    month = time.month
    day = time.day

    if myclass_list_info.count() > 0:
        new_myclass = myclass_list_info[0]
        new_myclass.play = 'A'
        new_myclass.play_time = str(year) + "-" + str(month) + "-" + str(day)
        new_myclass.play_video = prdCode + "|" + data

        period = myclass_list_info[0].prd.period * 30  # preiod * 개월(30)
        expireTime = time + timezone.timedelta(hours=9, days=period)
        new_myclass.expire_time = expireTime
        new_myclass.save()

    return HttpResponse(200)
