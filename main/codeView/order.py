from django.shortcuts import render
from main.query import *
from main.models import *
import string
import random

message_no_login = 210

import logging
logger = logging.getLogger(__name__)

def order_page(request):
    session = request.session.get('client_id')
    userid = request.session.get('user_id', '')  # 이 값으로 디비에서 정보찾고..
    if userid == '':
        logger.debug('user is not. use session:'.format(session))
        order_info = select_order(session)
        user_info = ''
        coupon_info = ''
        user = "n"
    else:
        logger.debug('user is exist.user:'.format(userid))
        if checkSession(session, userid):
            logger.debug('session is active')
            order_info = select_order(userid)
            user = "y"
            user_info = select_register(userid)
            coupon_info = select_myCoupon_notUsed(userid)

        else:
            logger.debug('session is deactive')
            disableSession(userid, request)
            return render(request, 'login/login.html')

    delivery = 0
    if order_info.count() > 0:
        delivery = order_info[0].delivery_price

    payway_info = select_payway()
    request.session['order_count'] = order_info.count()
    context = {
        "order_detail": order_info,
        "user_detail": user_info,
        "coupon_detail": coupon_info,
        "pay_result": '',
        "pay_msg": '',
        "user": user,
        "delivery_price": delivery,
        "payway_info":payway_info,

    }
    return render(request, 'payment/order.html', context)  # templete에 없으면 호출이 안됨. ajax

def order(request):
    session = request.session.get('client_id')
    logger.debug('session:'.format(session))
    if session is None:
        logger.debug('session is nullable')
        number_pool = string.digits
        _LENGTH = 8
        session = str(timezone.now().month) + str(timezone.now().day) + str(timezone.now().hour) + str(timezone.now().minute) + "-"
        for i in range(_LENGTH):
            session += random.choice(number_pool)
        request.session['client_id'] = session

    logger.debug('session is : '.format(session))

    #prd_code = request.POST['prd_code']
    flag = int(request.POST['flag'])
    option1 = int(request.POST['option1'])
    option2 = int(request.POST['option2'])
    option3 = int(request.POST['option3'])
    count = int(request.POST['count'])
    prd_code = request.POST['option_level']

    messages = 0
    user_id = request.session.get('user_id', '')
    if user_id == '':
        order_prd_info = select_order_prdCode(session, prd_code)
        if order_prd_info.count() > 0:  # 장바구니에 같은 prd가 있으면 count +
            update_order_prdCode(order_prd_info, count, option1, option2, option3)
            messages = 1  # 성공
        else:
            prd_info = select_prd(prd_code)
            order_info = OrderTB(user_id=session, prd=prd_info[0], option1_selectNum=option1, option2_selectNum=option2,
                                 option3_selectNum=option3, count=count)
            order_info.save()
            messages = 1  # 성공

            new_order_info = select_order(session)
            request.session['order_count'] = new_order_info.count()

    else:
        # login_info = select_login(user_id)
        order_prd_info = select_order_prdCode(user_id, prd_code)
        if order_prd_info.count() > 0:  # 장바구니에 같은 prd가 있으면 count +
            update_order_prdCode(order_prd_info, count, option1, option2, option3)
            messages = 1  # 성공
        else:
            prd_info = select_prd(prd_code)
            order_info = OrderTB(user_id=user_id, prd=prd_info[0], option1_selectNum=option1, option2_selectNum=option2,
                                 option3_selectNum=option3, count=count)

            order_info.save()
            messages = 1  # 성공

            new_order_info = select_order(user_id)
            request.session['order_count'] = new_order_info.count()

    if flag == 1:
        items_info = select_class_detail(prd_code)
        if items_info.count() > 0:
            html_file = "product/" + items_info[0].prd.tag + ".html"
            prd_tag = select_prd_tag(items_info[0].prd.tag)
        context = {
            "message": messages,
            "prd_tag": prd_tag,
            "prd_detail": items_info[0].prd,
            "html_file":html_file,
        }
        return render(request, 'class/class_detail.html', context)

    elif flag == 2:
        return order_page(request)

def order_delete(request):
    order_idx = request.POST['order_idx']
    user_id = request.session.get('user_id', '')
    session = request.session.get('client_id')

    split_order = order_idx.split(',')

    for idx in split_order:
        if len(idx) > 0:
            if user_id == '':
                order_info = select_order_idx(idx, session)
                if order_info.count() > 0:
                    delete_order_idx(order_info, '')
            else:
                order_info = select_order_idx(idx, user_id)
                if order_info.count() > 0:
                    delete_order_idx(order_info, '')

    delivery = 0
    if user_id == '':
        new_order_info = select_order(session)
        user_info = ''
        coupon_info = ''
        user = 'n'
    else:
        new_order_info = select_order(user_id)
        user_info = select_register(user_id)
        coupon_info = select_myCoupon_notUsed(user_id)
        user = 'y'

    payway_info = select_payway()
    request.session['order_count'] = new_order_info.count()

    if new_order_info.count() is not 0:
        delivery = new_order_info[0].delivery_price

    context = {
        "order_detail": new_order_info,
        "user_detail": user_info,
        "coupon_detail": coupon_info,
        "pay_result": '',
        "pay_msg": '',
        "user": user,
        "delivery_price": delivery,
        "payway": payway_info,
    }

    return render(request, 'payment/order.html', context)  # templete에 없으면 호출이 안됨. ajax