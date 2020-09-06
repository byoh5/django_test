from django.shortcuts import render
from main.query import *
from main.models import *


pay_ok = 0
pay_fail = 1

def payment(request):
    user_id = request.session.get('user_id')
    order_len = request.POST['len']
    addr_num = request.POST['addr_num']
    prd_price = int(request.POST['total_prd_price'])
    option_price = int(request.POST['total_option_price'])
    prd_total_price = int(request.POST['total_option_prd_price'])

    order_list = ""
    prd_title = ""
    prd_total_count = 0

    for cnt in range(int(order_len)):
        idx = request.POST['orderIdxs_' + str(cnt)]
        prd_count = request.POST['prodQuantity_' + str(cnt)]
        prd_total_count += int(prd_count)
        prd_title = update_order_idx(idx, user_id, prd_count, addr_num)  # count 변경 되었을 수 있으니 and 선택된 배송지 번호 정보 update 및 상품 title get
        order_list += idx + ","

    if prd_total_count > 1:
        prd_title += "_외 " + str(prd_total_count) + "개"

    regi_info = select_register(user_id)

    if regi_info.count() is not 0:
        if int(addr_num) == 1:
            addr = regi_info[0].regi_receiver1_add02 + " " + regi_info[0].regi_receiver1_add03 + "(" + regi_info[0].regi_receiver1_add01 + ")"
        else:
            addr = regi_info[0].regi_receiver2_add02 + " " + regi_info[0].regi_receiver2_add03 + "(" + regi_info[
                0].regi_receiver2_add01 + ")"

        pay_info = PayTB(user_id=user_id, pay_user=regi_info[0], order_id=order_list, prd_info=prd_title,
                         prd_price=prd_price, delivery_price=option_price, prd_total_price=prd_total_price,
                         delivery_addr=addr)
        pay_info.save()

        context = {
            "payment": pay_info,
        }

        return render(request, 'payment/pay_info.html', context)


def pay_result(request):
    pay_idx = int(request.POST['pay'])
    user_id = request.session.get('user_id')

    pay_result = int(request.POST['pay_result'])
    pay_msg = request.POST['pay_msg']

    pay_info = select_pay(pay_idx)

    if pay_info.count() is not 0:
        update_pay = pay_info[0]
        update_pay.pay_result_info = pay_msg
        update_pay.pay_result = pay_result

        if pay_result == pay_ok:
            split_order = update_pay.order_id.split(',')

            # product -> myclass에 넣고, 장바구니 정리하기
            for data in split_order:
                if len(data) > 0:
                    order_info = select_order_idx(data, user_id)

                    if order_info.count() is not 0:
                        # insert myclass_list
                        period = order_info[0].prd.period * 60
                        expireTime = timezone.now() + timezone.timedelta(days=period)
                        myclass_list_info = MyClassListTB(user_id=user_id, prd=order_info[0].prd,
                                                          expire_time=expireTime)
                        myclass_list_info.save()

                    delete_order_idx(order_info)  # order dbstat 변경

        update_pay.save()

    if pay_result == pay_ok:
        myclass_list_info = select_myclass_list(user_id)

        context = {
            "myclass_list_detail": myclass_list_info,
        }

        return render(request, 'myclass/myclass_list.html', context)
    else:
        order_info = select_order(user_id)
        user_info = select_register(user_id)
        context = {
            "order_detail": order_info,
            "user_detail": user_info,
            "pay_result": pay_result,
            "pay_msg": pay_msg,
        }

        return render(request, 'payment/order.html', context)
