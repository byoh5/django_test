from django.shortcuts import render
from django.utils import timezone

from main.query import *
from main.models import *
import string
import random
import requests
import json
from collections import OrderedDict
pay_ok = 0
pay_fail = 1

pay_status_ok = 1
pay_status_delivery = 2
pay_status_delivery_done = 3
pay_status_prepay = 4
pay_status_deposit_noCheck = 5
pay_status_deposit_refund = 6
pay_status_deposit_refund_req = 7

imp_id = 'imp08800373'

payway_credit = 'credit'
payway_escrow = 'escrow' #실시간 계좌이체
payway_deposit = 'deposit' #무통장
payway_naver = 'naverco'

nouser = 'kcp_nouser' #비회원

def payment(request):
    user_id = request.session.get('user_id', '')
    pg_type = request.POST['pg_type']
    delivery = 3000

    if pg_type == 'naverco':
        payway_info = select_payway_value_all(pg_type)
        return pay_naver(request, payway_info)

    if user_id == '':
        order_info = select_order(user_id)
        user_info = select_register(user_id)
        request.session['order_count'] = order_info.count()
        context = {
            "order_detail": order_info,
            "user_detail": user_info,
            "pay_result": "로그인이 필요합니다.",
            "pay_msg": pay_fail,
            "delivery_price": delivery,
        }

        return render(request, 'payment/order.html', context)

    else:
        number_pool = string.digits
        _LENGTH = 12
        pay_num = str(timezone.now().year) + str(timezone.now().month) + str(timezone.now().day) \
                  + str(timezone.now().hour) + str(timezone.now().minute) + str(timezone.now().second) + "-"
        for i in range(_LENGTH):
            pay_num += random.choice(number_pool)  # 랜덤한 문자열 하나 선택

        order_list = ""
        prd_total_count = 0
        option1 = "0"
        option2 = "0"
        option3 = "0"

        order_cnt = request.POST['idx']
        prd_price = int(request.POST['total_prd_price'])
        delivery_price = int(request.POST['total_delivery_price'])
        prd_total_price = int(request.POST['total_option_prd_price'])

        split_order = order_cnt.split(',')

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
                    # count 변경 되었을 수 있으니 and 선택된 배송지 번호 정보 update 및 상품 title get
                    update_order_idx(prd_count, order_info, option1, option2, option3, pay_num)

                    order_list += idx + ","

        user_info = select_register(user_id)
        payway_info = select_payway()
        coupon_info = select_myCoupon_notUsed(user_id)
        order_info = select_order_payNum(pay_num, user_id)

        context = {
            "order_detail": order_info,
            "order_list": order_list,
            "order_count": order_info.count(),
            "user_detail": user_info,
            "prd_price": prd_price,
            "delivery_price": delivery_price,
            "prd_total_price": prd_total_price,
            "payway_info":payway_info,
            "coupon_detail": coupon_info,
            "pay_num":pay_num,
        }

        return render(request, 'payment/payment.html', context)

def payment_ing(request):
    user_id = request.session.get('user_id')
    payway_val = request.POST.get('payway', '0')
    pay_num = request.POST.get('pay_num', '0')

    if payway_val == 0:
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
        payway_info = select_payway_value(payway_val)

        delivery = 0
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
            if order_info.count() is not 0:
                delivery = order_info[0].delivery_price
            context = {
                "order_detail": order_info,
                "user_detail": user_info,
                "coupon_detail": coupon_info,
                "pay_result": pay_result,
                "pay_msg": pay_fail,
                "user": 'y',
                "delivery_price": delivery,
                "payway_info": payway_info_all,
            }

            return render(request, 'payment/order.html', context)



def pay_deposit(request, payway_info, pay_num):
    user_id = request.session.get('user_id')
    addr_num = request.POST['addr_num']
    prd_price = int(request.POST['total_prd_price'])
    delivery_price = int(request.POST['total_delivery_price'])
    prd_total_price = int(request.POST['total_option_prd_price'])
    coupon_prd_total_price = int(request.POST['total_option_coupon_prd_price'])

    de_name = request.POST['depositName']
    de_receipt = request.POST['depositReceipt']

    order_list = request.POST.get('order_list', '0')
    prd_total_count = 0

    coupon_num = request.POST['coupon_num']
    if coupon_prd_total_price == 0:
        pay_price = prd_total_price
    else:
        pay_price = coupon_prd_total_price

    # product -> myclass에 넣고, 장바구니 정리하기

    order_info = select_order_payNum(pay_num, user_id)
    prd_title = order_info[0].prd.title

    for order in order_info:
        prd_total_count += order.count
        new_order = order
        new_order.addr_num = addr_num
        new_order.save()

        # insert myclass_list
        myclass_list_info = MyClassListTB(user_id=user_id, prd=order.prd, pay_num=pay_num,
                                          expire_time=timezone.now(), dbstat='D-deposit')

        myclass_list_info.save()

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
    session = request.session.get('client_id')

    addr_num = request.POST['addr_num']
    prd_price = int(request.POST['total_prd_price'])
    delivery_price = int(request.POST['total_delivery_price'])
    prd_total_price = int(request.POST['total_option_prd_price'])
    coupon_prd_total_price = int(request.POST['total_option_coupon_prd_price'])

    order_list = request.POST.get('order_list', '0')
    prd_total_count = 0

    coupon_num = request.POST['coupon_num']
    if coupon_prd_total_price == 0:
        pay_price = prd_total_price
    else:
        pay_price = coupon_prd_total_price

    order_info = select_order_payNum(pay_num, user_id)
    prd_title = order_info[0].prd.title

    for order in order_info:
        prd_total_count += order.count
        new_order = order
        new_order.addr_num = addr_num
        new_order.save()

    if prd_total_count > 1:
        prd_title += "_외 " + str(prd_total_count) + "개"

    pay_userStatus_info = select_userStatue(pay_status_prepay)
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

def pay_escrow(request, payway_info, pay_num):
    user_id = request.session.get('user_id')
    addr_num = request.POST['addr_num']
    prd_price = int(request.POST['total_prd_price'])
    delivery_price = int(request.POST['total_delivery_price'])
    prd_total_price = int(request.POST['total_option_prd_price'])
    coupon_prd_total_price = int(request.POST['total_option_coupon_prd_price'])

    es_name = request.POST['escrowName']
    es_receipt = request.POST['escrowReceipt']

    order_list = request.POST.get('order_list', '0')
    prd_total_count = 0

    coupon_num = request.POST['coupon_num']
    if coupon_prd_total_price == 0:
        pay_price = prd_total_price
    else:
        pay_price = coupon_prd_total_price

    order_info = select_order_payNum(pay_num, user_id)
    prd_title = order_info[0].prd.title

    for order in order_info:
        prd_total_count += order.count
        new_order = order
        new_order.addr_num = addr_num
        new_order.save()

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

def merge_dic(x, y):
    z = x.copy()
    z.update(y)
    return z

def naverpay_prd_text(order_info):
    count = str(order_info[0].count)
    prd_price = str(order_info[0].prd.price)
    prd_title = order_info[0].prd.title
    prd_code = order_info[0].prd.prd_code
    delivery_price = str(order_info[0].delivery_price)
    keyword = str(order_info[0].prd.keyword)

    shipping_data = OrderedDict()
    shipping_data['groupId'] = 'shipping_' + prd_code
    shipping_data['method'] = 'DELIVERY'
    shipping_data['baseFee'] = delivery_price
    shipping_data['feeRule'] = {'area': 'jeju','surcharge': 5000}
    shipping_data['feePayType'] = 'PREPAYED'

    selections_data = OrderedDict()
    selections_data['code'] = keyword
    selections_data['label'] = '레벨'
    selections_data['value'] = keyword

    options_data = OrderedDict()
    options_data['optionQuantity'] = count
    options_data['optionPrice'] = 0
    options_data['selections'] = selections_data,

    supplemets_list = []
    if order_info[0].option1_selectNum == 2:
        supplements1_data = OrderedDict()
        supplements1_data['id'] = prd_code + '_1'
        supplements1_data['name'] = order_info[0].prd.option1
        supplements1_data['price'] = order_info[0].prd.option1_price
        supplements1_data['quantity'] = count
        supplemets_list.append(supplements1_data)

    if order_info[0].option2_selectNum == 2:
        supplements2_data = OrderedDict()
        supplements2_data['id'] = prd_code + '_2'
        supplements2_data['name'] = order_info[0].prd.option2
        supplements2_data['price'] = order_info[0].prd.option2_price
        supplements2_data['quantity'] = count
        supplemets_list.append(supplements2_data)

    if order_info[0].option3_selectNum == 2:
        supplements3_data = OrderedDict()
        supplements3_data['id'] = prd_code + '_3'
        supplements3_data['name'] = order_info[0].prd.option3
        supplements3_data['price'] = order_info[0].prd.option3_price
        supplements3_data['quantity'] = count
        supplemets_list.append(supplements3_data)

    prd_data = OrderedDict()
    prd_data["id"] = prd_code
    prd_data["name"] = prd_title
    prd_data["basePrice"] = prd_price
    prd_data["taxType"] = 'TAX'
    prd_data["quantity"] = count
    prd_data["infoUrl"] = 'http://runcoding.co.kr/detail_prd/?prd_code=' + order_info[0].prd.prd_code
    prd_data["img_url"] = 'http://runcoding.co.kr' + order_info[0].prd.img
    prd_data["shipping"] = shipping_data
    prd_data["options"] = options_data,
    prd_data["supplements"] = supplemets_list

    return prd_data

def pay_naver(request, payway_info):
    session = request.session.get('client_id')
    user_id = request.session.get('user_id')
    order_idx = request.POST['idx']
    prd_price = request.POST['total_prd_price']
    delivery_price = request.POST['total_delivery_price']
    pay_price = request.POST['total_option_prd_price']

    order_list = ""
    prd_title = ""
    prd_total_count = 0
    option1 = "0"
    option2 = "0"
    option3 = "0"
    coupon_num = ""


    number_pool = string.digits
    _LENGTH = 12
    pay_num = str(timezone.now().year) + str(timezone.now().month) + str(timezone.now().day) \
              + str(timezone.now().hour) + str(timezone.now().minute) + str(timezone.now().second) + "-"
    for i in range(_LENGTH):
        pay_num += random.choice(number_pool)  # 랜덤한 문자열 하나 선택


    split_order = order_idx.split(',')
    prd_list = []

    # product -> myclass에 넣고, 장바구니 정리하기
    for data in split_order:
        if len(data) > 0:
            idx = request.POST['orderIdxs_' + str(data)]
            prd_count = request.POST['prodQuantity_' + str(data)]

            if user_id == "":
                order_info = select_order_idx(idx, session)
            else:
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

                # count 변경 되었을 수 있으니 and 선택된 배송지 번호 정보 update 및 상품 title get
                update_order_idx(prd_count, order_info, option1, option2, option3, pay_num)
                order_list += idx + ","

                #prd_list.append(naverpay_prd_text(order_info))


    if prd_total_count > 1:
        prd_title += "_외 " + str(prd_total_count) + "개"

    if user_id == "":
        pay_user = ""
    else:
        regi_info = select_register(user_id)
        pay_user = regi_info[0]

    pay_userStatus_info = select_userStatue(pay_status_prepay)
    pay_info = PayTB(pay_num=pay_num, pay_user=pay_user, order_id=order_list, coupon_num=coupon_num,
                     prd_info=prd_title, pay_user_status=pay_userStatus_info[0],
                     prd_price=int(prd_price), delivery_price=int(delivery_price), prd_total_price=int(pay_price),
                     delivery_name="runcoding", delivery_addr="경기도 수원시", delivery_phone="01012341234", payWay=payway_info[0])
    pay_info.save()

    if user_id == "":
        order_info = select_order_payNum(pay_num, session)
    else:
        order_info = select_order_payNum(pay_num, user_id)

    # pay_data = OrderedDict()
    # pay_data['pg'] = 'naverco'
    # pay_data["pay_method"] = 'card'
    # pay_data["merchant_uid"] = 'merchant_' + pay_num
    # pay_data["name"] = prd_title
    # pay_data["amount"] = pay_price
    # pay_data["buyer_email"] = 'iamport@siot.do'
    # pay_data["buyer_name"] = 'runcoding'
    # pay_data["buyer_tel"] = '01012341234'
    # pay_data["buyer_addr"] = '경기도 수원시 영통구'
    # pay_data["buyer_postcode"] = '123-456'
    # pay_data["naverProducts"] = prd_list




    context = {
        "payment": pay_info,
        "order_info": order_info,
        "count": order_info.count(),
        "imp": imp_id,
        #"text_data": test,
    }

    return render(request, 'payment/pay_naver.html', context)

def pay_result(request):
    pay_idx = int(request.POST['pay'])
    user_id = request.session.get('user_id', '')
    session = request.session.get('client_id')

    pay_result = int(request.POST['pay_result'])
    pay_msg = request.POST['pay_msg']

    merchant_uid = request.POST['merchant_uid']
    imp_uid = request.POST['imp_uid']
    card_apply = request.POST['card_apply']

    pay_info = select_pay(pay_idx)
    payway_info = select_payway()

    if pay_info.count() is not 0:
        update_pay = pay_info[0]
        update_pay.pay_result_info = pay_msg
        update_pay.pay_result = pay_result
        update_pay.merchant_uid = merchant_uid
        update_pay.card_apply = card_apply
        update_pay.imp_uid = imp_uid

        if pay_result == pay_ok:
            pay_userStatus_info = select_userStatue(pay_status_ok) # 구매성공
            if pay_info[0].coupon_num != '0':
                update_myCoupon(user_id, pay_info[0].coupon_num)
            update_pay.pay_user_status = pay_userStatus_info[0]
            split_order = pay_info[0].order_id.split(',')

            # product -> myclass에 넣고, 장바구니 정리하기

            for data in split_order:
                if len(data) > 0:
                    if user_id == '':
                        order_info = select_order_idx(data, session)
                        if order_info.count() > 0:
                            myclass_list_info = MyClassListTB(user_id=pay_info[0].pay_email, prd=order_info[0].prd,
                                                              pay_num=pay_info[0].pay_num,
                                                              expire_time=timezone.now())
                            myclass_list_info.save()
                            delete_order_idx(order_info, pay_info[0].pay_num)  # order dbstat 변경
                    else:
                        order_info = select_order_idx(data, user_id)
                        if order_info.count() > 0:
                            item_info = select_item_group(order_info[0].prd.prd_code)
                            for item in item_info:
                                myclass_list_info = MyClassListTB(user_id=user_id, prd=order_info[0].prd,
                                                                  pay_num=pay_info[0].pay_num, item_code=item['item_code'],
                                                                  expire_time=timezone.now())
                                myclass_list_info.save()
                            delete_order_idx(order_info, pay_info[0].pay_num)  # order dbstat 변경

            update_pay.save()

            if user_id == '':
                new_order_info = select_order(session)
                request.session['order_count'] = new_order_info.count()

                pay_user_info = select_pay_paynum(pay_info[0].pay_num)
                context = {
                    "user_detail": pay_user_info,
                }
                return render(request, 'mypage/myorder_noUser.html', context)
            else:
                myclass_list_info = select_myclass_list(user_id)
                new_order_info = select_order(user_id)
                request.session['order_count'] = new_order_info.count()

                context = {
                    "myclass_list_detail": myclass_list_info,
                }

                return render(request, 'myclass/myclass_list.html', context)
        else:
            delivery_price = 0
            if user_id == '':
                order_info = select_order(session)
                request.session['order_count'] = order_info.count()

                if order_info.count() > 0:
                    delivery_price = order_info[0].delivery_price

                context = {
                    "order_detail": order_info,
                    "user_detail": '',
                    "coupon_detail": '',
                    "pay_result": pay_result,
                    "pay_msg": pay_msg,
                    "user": 'n',
                    "delivery_price": delivery_price,
                    "payway_info": payway_info,
                }
            else:
                order_info = select_order(user_id)
                user_info = select_register(user_id)
                coupon_info = select_myCoupon_notUsed(user_id)
                request.session['order_count'] = order_info.count()

                if order_info.count() > 0:
                    delivery_price = order_info[0].delivery_price

                context = {
                    "order_detail": order_info,
                    "user_detail": user_info,
                    "coupon_detail": coupon_info,
                    "pay_result": pay_result,
                    "pay_msg": pay_msg,
                    "user": 'y',
                    "delivery_price": delivery_price,
                    "payway_info": payway_info,
                }

            return render(request, 'payment/order.html', context)

def refund(refund_info, refund_price):
    runcoding = select_runcoding()

    key = runcoding[0].imp_key
    secret = runcoding[0].imp_secret

    run_uid = refund_info[0].imp_uid
    price = refund_price
    run_reason = '사용자요청'

    # getToken
    post_data = {
        'imp_key': key,
        'imp_secret': secret
    }
    token_msg = requests.post(url='https://api.iamport.kr/users/getToken', data=json.dumps(post_data),
                              headers={'Content-Type': 'application/json'})

    json_msg = token_msg.json()
    json_res = json_msg["response"]
    access_token = json_res["access_token"]

    # get auth user
    post_data_cancle = {
        'amount': price,
        'reason':run_reason,
        'imp_uid':run_uid
    }
    cancle_user_msg = requests.post(url='https://api.iamport.kr/payments/cancel/', data=json.dumps(post_data_cancle),
                                    headers={'Content-Type': 'application/json', 'Authorization': access_token})
    json_user_msg = cancle_user_msg.json()
    json_user_msg_res = json_user_msg["response"]
    json_user_msg_code = json_user_msg["code"]

    if json_user_msg_code == 1: #이미취소된
        return json_user_msg_code
    elif json_user_msg_code == 0:
        return json_user_msg_res



