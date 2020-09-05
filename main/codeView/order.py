from django.shortcuts import render
from main.query import *
from main.models import *


def order_page(request):
    session = request.session.get('client_id')
    userid = request.session.get('user_id')  # 이 값으로 디비에서 정보찾고..
    if session is None:
        return render(request, 'login/login.html')
    else:
        order_info = select_order(userid)
        user_info = select_register(userid)
        context = {
            "order_detail": order_info,
            "user_detail": user_info,
            "pay_result": '',
            "pay_msg": '',
        }
        return render(request, 'payment/order.html', context)  # templete에 없으면 호출이 안됨. ajax

def order(request):
    user_id = request.session.get('user_id')
    prd_code = request.POST['prd_code']
    login_info = select_login(user_id)
    messages = 0
    if login_info.count() is not 0:
        order_prd_info = select_order_prdCode(user_id, prd_code)
        if order_prd_info.count() is not 0:
            update_order_prdCode(order_prd_info)
            messages = 1  # 성공
        else:
            prd_info = select_prd(prd_code)
            order = OrderTB(user_id=user_id, prd_code=prd_code, prd=prd_info[0])
            order.save()
            messages = 1  # 성공

    items_info = select_class_detail(prd_code)
    context = {
        "message": messages,
        "class_items_detail": items_info,
        "prd_detail": items_info[0].prd,
    }
    return render(request, 'class/class_detail.html', context)
