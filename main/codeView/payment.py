from django.shortcuts import render
from django.utils import timezone
from main.query import *
from main.models import *
import string
import random

pay_ok = 0
pay_fail = 1

pay_status_ok = 1
pay_status_delivery = 2
pay_status_delivery_done = 3
pay_status_prepay = 4
pay_status_deposit_noCheck = 5

imp_id = 'imp08800373'

payway_credit = 'credit'
payway_escrow = 'escrow' #실시간 계좌이체
payway_deposit = 'deposit' #무통장
payway_kakao = 'kakao'
payway_naver = 'naver'


def payment(request):
    payway_val = request.POST['payway']
    user_id = request.session.get('user_id')
    if payway_val is not None:
        payway_info = select_payway_value(payway_val)

        number_pool = string.digits
        _LENGTH = 12
        pay_num = str(timezone.now().year) + str(timezone.now().month) + str(timezone.now().day) \
                  + str(timezone.now().hour) + str(timezone.now().minute) + str(timezone.now().second) + "-"
        for i in range(_LENGTH):
            pay_num += random.choice(number_pool)  # 랜덤한 문자열 하나 선택

        if payway_info.count() > 0 and payway_info[0].value == payway_credit:
            return pay_credit(request, payway_info, pay_num)
        elif payway_info.count() > 0 and payway_info[0].value == payway_deposit:
            return pay_deposit(request, payway_info, pay_num)
        elif payway_info.count() > 0 and payway_info[0].value == payway_escrow:
            return pay_escrow(request, payway_info, pay_num)
        else:
            order_info = select_order(user_id)
            user_info = select_register(user_id)
            coupon_info = select_myCoupon_notUsed(user_id)
            payway_info_all = select_payway()
            request.session['order_count'] = order_info.count()
            context = {
                "order_detail": order_info,
                "user_detail": user_info,
                "coupon_detail": coupon_info,
                "pay_result": pay_result,
                "pay_msg": pay_fail,
                "delivery_price": order_info[0].delivery_price,
                "payway_info": payway_info_all,
            }

            return render(request, 'payment/order.html', context)

    else:
        return render(request, 'login/login.html')

def pay_deposit(request, payway_info, pay_num):
    user_id = request.session.get('user_id')
    order_idx = request.POST['idx']
    addr_num = request.POST['addr_num']
    prd_price = int(request.POST['total_prd_price'])
    delivery_price = int(request.POST['total_delivery_price'])
    prd_total_price = int(request.POST['total_option_prd_price'])
    coupon_prd_total_price = int(request.POST['total_option_coupon_prd_price'])

    de_name = request.POST['depositName']
    de_receipt = request.POST['depositReceipt']

    order_list = ""
    prd_title = ""
    prd_total_count = 0
    option1 = "0"
    option2 = "0"
    option3 = "0"

    coupon_num = request.POST['coupon_num']
    if coupon_prd_total_price == 0:
        pay_price = prd_total_price
    else:
        pay_price = coupon_prd_total_price

    split_order = order_idx.split(',')

    # product -> myclass에 넣고, 장바구니 정리하기
    for data in split_order:
        if len(data) > 0:
            idx = request.POST['orderIdxs_' + str(data)]
            prd_count = request.POST['prodQuantity_' + str(data)]

            order_info = select_order_idx(idx, user_id)
            if order_info.count() > 0:
                if order_info[0].prd.option1 != "":
                    option1 = request.POST['option_idx_' + str(data) + "_1"]
                if order_info[0].prd.option2 != "":
                    option2 = request.POST['option_idx_' + str(data) + "_2"]
                if order_info[0].prd.option3 != "":
                    option3 = request.POST['option_idx_' + str(data) + "_3"]

                prd_total_count += int(prd_count)
                prd_title = order_info[0].prd.title
                update_order_idx(prd_count, order_info, addr_num, option1, option2, option3, pay_num)  # count 변경 되었을 수 있으니 and 선택된 배송지 번호 정보 update 및 상품 title get
                order_list += idx + ","

            # insert myclass_list
            myclass_list_info = MyClassListTB(user_id=user_id, prd=order_info[0].prd, pay_num=pay_num,
                                              expire_time=timezone.now(), dbstat='D-deposit')
            myclass_list_info.save()

            delete_order_idx(order_info, pay_num)  # order dbstat 변경

    if prd_total_count > 1:
        prd_title += "_외 " + str(prd_total_count) + "개"

    regi_info = select_register(user_id)

    if regi_info.count() is not 0:
        if int(addr_num) == 1:
            phone = regi_info[0].regi_phone
            name = regi_info[0].regi_name
            addr = regi_info[0].regi_receiver1_add02 + " " + regi_info[0].regi_receiver1_add03 + "(" + regi_info[
                0].regi_receiver1_add01 + ")"
        else:
            name = regi_info[0].regi_receiver2_name
            phone = regi_info[0].regi_receiver2_phone
            addr = regi_info[0].regi_receiver2_add02 + " " + regi_info[0].regi_receiver2_add03 + "(" + regi_info[
                0].regi_receiver2_add01 + ")"

        pay_userStatus_info = select_userStatue(pay_status_deposit_noCheck)
        pay_info = PayTB(pay_num=pay_num, pay_user=regi_info[0], order_id=order_list, coupon_num=coupon_num,
                         prd_info=prd_title, pay_user_status=pay_userStatus_info[0],
                         payWay_name=de_name, payWay_receipt=de_receipt,
                         prd_price=prd_price, delivery_price=delivery_price, prd_total_price=pay_price,
                         delivery_name=name, delivery_addr=addr, delivery_phone=phone, payWay=payway_info[0])

        pay_info.save()

        new_order_info = select_order(user_id)
        request.session['order_count'] = new_order_info.count()
        pay_user_info = select_pay_user(user_id)
        context = {
            "user_detail": pay_user_info,
        }
        return render(request, 'mypage/myorder.html', context)
    else:
        return render(request, 'login/login.html')

def pay_credit(request, payway_info, pay_num):
    user_id = request.session.get('user_id')
    order_idx = request.POST['idx']
    addr_num = request.POST['addr_num']
    prd_price = int(request.POST['total_prd_price'])
    delivery_price = int(request.POST['total_delivery_price'])
    prd_total_price = int(request.POST['total_option_prd_price'])
    coupon_prd_total_price = int(request.POST['total_option_coupon_prd_price'])

    order_list = ""
    prd_title = ""
    prd_total_count = 0
    option1 = "0"
    option2 = "0"
    option3 = "0"

    coupon_num = request.POST['coupon_num']
    if coupon_prd_total_price == 0:
        pay_price = prd_total_price
    else:
        pay_price = coupon_prd_total_price

    split_order = order_idx.split(',')

    # product -> myclass에 넣고, 장바구니 정리하기
    for data in split_order:
        if len(data) > 0:
            idx = request.POST['orderIdxs_' + str(data)]
            prd_count = request.POST['prodQuantity_' + str(data)]

            order_info = select_order_idx(idx, user_id)
            if order_info.count() > 0:
                if order_info[0].prd.option1 != "":
                    option1 = request.POST['option_idx_' + str(data) + "_1"]
                if order_info[0].prd.option2 != "":
                    option2 = request.POST['option_idx_' + str(data) + "_2"]
                if order_info[0].prd.option3 != "":
                    option3 = request.POST['option_idx_' + str(data) + "_3"]

                prd_total_count += int(prd_count)
                prd_title = order_info[0].prd.title
                update_order_idx(prd_count, order_info, addr_num, option1, option2, option3, pay_num)  # count 변경 되었을 수 있으니 and 선택된 배송지 번호 정보 update 및 상품 title get
                order_list += idx + ","

    if prd_total_count > 1:
        prd_title += "_외 " + str(prd_total_count) + "개"

    regi_info = select_register(user_id)

    if regi_info.count() is not 0:
        if int(addr_num) == 1:
            phone = regi_info[0].regi_phone
            name = regi_info[0].regi_name
            addr = regi_info[0].regi_receiver1_add02 + " " + regi_info[0].regi_receiver1_add03 + "(" + regi_info[
                0].regi_receiver1_add01 + ")"
        else:
            name = regi_info[0].regi_receiver2_name
            phone = regi_info[0].regi_receiver2_phone
            addr = regi_info[0].regi_receiver2_add02 + " " + regi_info[0].regi_receiver2_add03 + "(" + regi_info[
                0].regi_receiver2_add01 + ")"

        pay_userStatus_info = select_userStatue(pay_status_prepay)
        pay_info = PayTB(pay_num=pay_num, pay_user=regi_info[0], order_id=order_list, coupon_num=coupon_num,
                         prd_info=prd_title, pay_user_status=pay_userStatus_info[0],
                         prd_price=prd_price, delivery_price=delivery_price, prd_total_price=pay_price,
                         delivery_name=name, delivery_addr=addr, delivery_phone=phone, payWay=payway_info[0])
        pay_info.save()

        context = {
            "payment": pay_info,
            "imp": imp_id,
            "pay_method": 'card'
        }

        return render(request, 'payment/pay_info.html', context)
    else:
        return render(request, 'login/login.html')


def pay_escrow(request, payway_info, pay_num):
    user_id = request.session.get('user_id')
    order_idx = request.POST['idx']
    addr_num = request.POST['addr_num']
    prd_price = int(request.POST['total_prd_price'])
    delivery_price = int(request.POST['total_delivery_price'])
    prd_total_price = int(request.POST['total_option_prd_price'])
    coupon_prd_total_price = int(request.POST['total_option_coupon_prd_price'])

    es_name = request.POST['escrowName']
    es_receipt = request.POST['escrowReceipt']

    order_list = ""
    prd_title = ""
    prd_total_count = 0
    option1 = "0"
    option2 = "0"
    option3 = "0"

    coupon_num = request.POST['coupon_num']
    if coupon_prd_total_price == 0:
        pay_price = prd_total_price
    else:
        pay_price = coupon_prd_total_price

    split_order = order_idx.split(',')

    # product -> myclass에 넣고, 장바구니 정리하기
    for data in split_order:
        if len(data) > 0:
            idx = request.POST['orderIdxs_' + str(data)]
            prd_count = request.POST['prodQuantity_' + str(data)]

            order_info = select_order_idx(idx, user_id)
            if order_info.count() > 0:
                if order_info[0].prd.option1 != "":
                    option1 = request.POST['option_idx_' + str(data) + "_1"]
                if order_info[0].prd.option2 != "":
                    option2 = request.POST['option_idx_' + str(data) + "_2"]
                if order_info[0].prd.option3 != "":
                    option3 = request.POST['option_idx_' + str(data) + "_3"]

                prd_total_count += int(prd_count)
                prd_title = order_info[0].prd.title
                update_order_idx(prd_count, order_info, addr_num, option1, option2, option3, pay_num)  # count 변경 되었을 수 있으니 and 선택된 배송지 번호 정보 update 및 상품 title get
                order_list += idx + ","

    if prd_total_count > 1:
        prd_title += "_외 " + str(prd_total_count) + "개"

    regi_info = select_register(user_id)

    if regi_info.count() is not 0:
        if int(addr_num) == 1:
            phone = regi_info[0].regi_phone
            name = regi_info[0].regi_name
            addr = regi_info[0].regi_receiver1_add02 + " " + regi_info[0].regi_receiver1_add03 + "(" + regi_info[
                0].regi_receiver1_add01 + ")"
        else:
            name = regi_info[0].regi_receiver2_name
            phone = regi_info[0].regi_receiver2_phone
            addr = regi_info[0].regi_receiver2_add02 + " " + regi_info[0].regi_receiver2_add03 + "(" + regi_info[
                0].regi_receiver2_add01 + ")"

        pay_userStatus_info = select_userStatue(pay_status_prepay)
        pay_info = PayTB(pay_num=pay_num, pay_user=regi_info[0], order_id=order_list, coupon_num=coupon_num,
                         prd_info=prd_title, pay_user_status=pay_userStatus_info[0],
                         payWay_name=es_name, payWay_receipt=es_receipt,
                         prd_price=prd_price, delivery_price=delivery_price, prd_total_price=pay_price,
                         delivery_name=name, delivery_addr=addr, delivery_phone=phone, payWay=payway_info[0])
        pay_info.save()

        context = {
            "payment": pay_info,
            "imp": imp_id,
            "pay_method": 'trans'
        }

        return render(request, 'payment/pay_info.html', context)
    else:
        return render(request, 'login/login.html')


def pay_result(request):
    pay_idx = int(request.POST['pay'])
    user_id = request.session.get('user_id')

    pay_result = int(request.POST['pay_result'])
    pay_msg = request.POST['pay_msg']

    pay_info = select_pay(pay_idx)
    payway_info = select_payway()

    if pay_info.count() is not 0:
        update_pay = pay_info[0]
        update_pay.pay_result_info = pay_msg
        update_pay.pay_result = pay_result

        if pay_result == pay_ok:
            pay_userStatus_info = select_userStatue(pay_status_ok) # 구매성공
            if pay_info[0].coupon_num != '0':
                update_myCoupon(user_id, pay_info[0].coupon_num)
            update_pay.pay_user_status = pay_userStatus_info[0]
            split_order = update_pay.order_id.split(',')

            # product -> myclass에 넣고, 장바구니 정리하기
            for data in split_order:
                if len(data) > 0:
                    order_info = select_order_idx(data, user_id)

                    if order_info.count() is not 0:
                        # insert myclass_list
                        myclass_list_info = MyClassListTB(user_id=user_id, prd=order_info[0].prd, pay_num=pay_info[0].pay_num,
                                                          expire_time=timezone.now())
                        myclass_list_info.save()

                    delete_order_idx(order_info, pay_info[0].pay_num)  # order dbstat 변경

        update_pay.save()

    if pay_result == pay_ok:
        myclass_list_info = select_myclass_list(user_id)
        new_order_info = select_order(user_id)
        request.session['order_count'] = new_order_info.count()

        context = {
            "myclass_list_detail": myclass_list_info,
        }

        return render(request, 'myclass/myclass_list.html', context)
    else:
        order_info = select_order(user_id)
        user_info = select_register(user_id)
        coupon_info = select_myCoupon_notUsed(user_id)
        request.session['order_count'] = order_info.count()
        context = {
            "order_detail": order_info,
            "user_detail": user_info,
            "coupon_detail": coupon_info,
            "pay_result": pay_result,
            "pay_msg": pay_msg,
            "delivery_price": order_info[0].delivery_price,
            "payway_info": payway_info,
        }

        return render(request, 'payment/order.html', context)
