from django.shortcuts import render
from main.query import *
from main.models import *

message_no_login = 210

def order_page(request):
    session = request.session.get('client_id')
    userid = request.session.get('user_id')  # 이 값으로 디비에서 정보찾고..
    if session is None:
        return render(request, 'login/login.html')
    else:
        if checkSession(session, userid):
            order_info = select_order(userid)
            delivery = 0
            if order_info.count() is not 0:
                delivery = order_info[0].delivery_price
            user_info = select_register(userid)
            coupon_info = select_myCoupon_notUsed(userid)
            payway_info = select_payway()
            request.session['order_count'] = order_info.count()
            context = {
                "order_detail": order_info,
                "user_detail": user_info,
                "coupon_detail": coupon_info,
                "pay_result": '',
                "pay_msg": '',
                "delivery_price": delivery,
                "payway_info":payway_info,

            }
            return render(request, 'payment/order.html', context)  # templete에 없으면 호출이 안됨. ajax
        else:
            disableSession(userid, request)
            context = {
                "msg": message_no_login,
            }
            return render(request, 'login/login.html', context)

def order(request):
    user_id = request.session.get('user_id')
    prd_code = request.POST['prd_code']
    flag = int(request.POST['flag'])
    option1 = request.POST['option1']
    option2 = request.POST['option2']
    option3 = request.POST['option3']
    count = request.POST['count']
    login_info = select_login(user_id)

    messages = 0
    if login_info.count() is not 0:
        order_prd_info = select_order_prdCode(user_id, prd_code)
        if order_prd_info.count() is not 0: # 장바구니에 같은 prd가 있으면 count +
            update_order_prdCode(order_prd_info, count, option1, option2, option3)
            messages = 1  # 성공
        else:
            prd_info = select_prd(prd_code)
            order = OrderTB(user_id=user_id, prd=prd_info[0], option1_selectNum=option1, option2_selectNum=option2, option3_selectNum=option3, count=count)
            order.save()
            messages = 1  # 성공

        new_order_info = select_order(user_id)
        request.session['order_count'] = new_order_info.count()

        if flag == 1:
            items_info = select_class_detail(prd_code)
            context = {
                "message": messages,
                "class_items_detail": items_info,
                "prd_detail": items_info[0].prd,
            }
            return render(request, 'class/class_detail.html', context)

        elif flag == 2:
            return order_page(request)
    else:
        return render(request, 'login/login.html')

def order_delete(request):
    order_idx = request.POST['order_idx']
    user_id = request.session.get('user_id')
    split_order = order_idx.split(',')

    for idx in split_order:
        if len(idx) > 0:
            order_info = select_order_idx(idx, user_id)
            delete_order_idx(order_info)

    new_order_info = select_order(user_id)
    delivery = 0
    if new_order_info.count() is not 0:
        delivery = new_order_info[0].delivery_price

    user_info = select_register(user_id)
    coupon_info = select_myCoupon_notUsed(user_id)
    payway_info = select_payway()
    request.session['order_count'] = new_order_info.count()
    context = {
        "order_detail": new_order_info,
        "user_detail": user_info,
        "coupon_detail": coupon_info,
        "pay_result": '',
        "pay_msg": '',
        "delivery_price": delivery,
        "payway": payway_info,
    }
    return render(request, 'payment/order.html', context)  # templete에 없으면 호출이 안됨. ajax