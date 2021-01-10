from django.shortcuts import render
from django.utils import timezone
from main.query import *
from main.models import *
import bcrypt
from main.codeView.stat import stat_menu_step

message_ok = 200
message_diff_pass = 202
message_no_regi = 204
message_exist_id = 208

message_coupon_ok = 300
message_coupon_diff = 302
message_coupon_expired = 304
message_coupon_already_used = 306
imp_id = 'imp08800373'

ay_status_deposit_refund = 6
pay_status_deposit_refund_req = 7

message_no_login = 210

def mypage_profile(request):
    user_id = request.session.get('user_id')
    session = request.session.get('client_id')

    stat_menu_step(request, "myprofile", "", "")

    if checkSession(session, user_id):
        user_info = select_register(user_id)
        context = {
            "user_detail": user_info,
            "imp": imp_id,
        }
        return render(request, 'mypage/myprofile.html', context)
    else:
        disableSession(user_id, request)
        context = {
            "msg": message_no_login,
        }
        return render(request, 'login/login.html', context)


def mypage_order(request):
    user_id = request.session.get('user_id')
    session = request.session.get('client_id')

    stat_menu_step(request, "myprofile", "myorder", "")

    if checkSession(session, user_id):
        pay_user_info = select_pay_user(user_id)
        context = {
            "user_detail": pay_user_info,
        }
        return render(request, 'mypage/myorder.html', context)
    else:
        disableSession(user_id, request)
        context = {
            "msg": message_no_login,
        }
        return render(request, 'login/login.html', context)

def mypage_order_detail(request):
    pay_idx = request.POST.get('pay_idx', 0)
    user_id = request.session.get('user_id')
    session = request.session.get('client_id')
    refund = 0
    myclass_info = ""

    if checkSession(session, user_id):
        pay_info = select_pay(pay_idx)
        mycoupon_name = ""
        option_name = ""
        delivery_time =""
        play_time = ""

        stat_menu_step(request, "myprofile", "myorder_deatil", pay_info[0].pay_num)

        if pay_info.count() > 0 :
            if pay_info[0].coupon_num != "" :
                mycoupon_info = select_myCoupon_couponNum(user_id, pay_info[0].coupon_num)
                if mycoupon_info.count() > 0:
                    mycoupon_name = mycoupon_info[0].coupon.coupon_name

            if pay_info[0].pay_user_status.userStatus_idx < 4: # 구매 성공 일때만
                myclass_info = select_myclass_list_paynum_noplay(user_id, pay_info[0].pay_num)
                if myclass_info.count() > 0:
                    if pay_info[0].delivery_time is not None : # 배송 됨
                        today = timezone.now()
                        refundTime = pay_info[0].delivery_time + timezone.timedelta(hours=9, days=9)
                        if today <= refundTime: # 오늘이 배송된지 9일이 지났는지 확인
                            refund = 1 # 영상을 보지 않았고, 배송 후 9일이 지나지 않은 시점 = refund 가능
                    else:
                        refund = 1 #영상을 보지 않았고, 배송 전 = refund 가능

            split_order = pay_info[0].order_id.split(',')
            # product -> myclass에 넣고, 장바구니 정리하기
            for data in split_order:
                if len(data) > 0:
                    order_info = select_order_info(data, user_id)
                    if order_info.count() > 0:
                        if order_info[0].option1_selectNum == 2:
                            option_name += order_info[0].prd.option1
                            option_name += " | "

                        if order_info[0].option2_selectNum == 2:
                            if option_name != "":
                                option_name += ","
                            option_name += order_info[0].prd.option2
                            option_name += " | "

                        if order_info[0].option3_selectNum == 2:
                            if option_name != "":
                                option_name += ","
                            option_name += order_info[0].prd.option3
                            option_name += " | "
            order_info = select_order_payNum(pay_info[0].pay_num, user_id)
            context = {
                "pay_detail": pay_info,
                "myclass": myclass_info,
                "order_info":order_info,
                "refund": refund,
                "delivery_time": delivery_time,
                "play_time": play_time,
                "mycoupon_name": mycoupon_name,
                "option":option_name,
            }
            return render(request, 'mypage/myorder_detail.html', context)
        else:
            return mypage_order(request)
    else:
        disableSession(user_id, request)
        context = {
            "msg": message_no_login,
        }
        return render(request, 'login/login.html', context)

def mypage_order_refund(request):
    user_id = request.session.get('user_id')
    pay_num = request.POST.get('pay_num', '0')

    stat_menu_step(request, "myorder_deatil", "refund", pay_num)
    if pay_num == '0':
        pay_user_info = select_pay_user(user_id)
        context = {
            "user_detail": pay_user_info,
        }
        return render(request, 'mypage/myorder.html', context)

    refund_info = select_refund_paynum(user_id, pay_num)
    if refund_info.count() > 0:
        pay_user_info = select_pay_user(user_id)
        context = {
            "user_detail": pay_user_info,
        }
        return render(request, 'mypage/myorder.html', context)

    pay_way = request.POST['pay_way']
    order_idx = request.POST['order_idx']
    account_val = ""
    if pay_way == 'deposit':
        bank = request.POST['bank']
        account = request.POST['account']
        account_val = bank + account

    pay_userStatus_info = select_userStatue(pay_status_deposit_refund_req)

    pay_info = select_pay_user_payNum(user_id, pay_num)
    new_payInfo = pay_info[0]
    new_payInfo.pay_result = 3 #환불요청
    new_payInfo.pay_user_status = pay_userStatus_info[0]
    # if pay_way == 'deposit':
    #     new_payInfo.payWay_account = bank + account # 모두 삭제
    new_payInfo.save()

    split_order = order_idx.split(',')
    for idx in split_order:
        if len(idx) > 0:
            order_info = select_order_info(idx, user_id)
            myclass_list = select_myclass_list_payNum_active(user_id, pay_num)
            for class_list in myclass_list:
                if class_list.prd.prd_code == order_info[0].prd.prd_code: #요청한 키트의 강의만 block
                    new_myclass = class_list
                    new_myclass.dbstat = 'D-refund'
                    new_myclass.save()

            option1_price = 0
            option2_price = 0
            option3_price = 0

            option1_name = ""
            option2_name = ""
            option3_name = ""
            if order_info[0].option1_selectNum == 2:
                option1_name = order_info[0].prd.option1
                option1_price = order_info[0].prd.option1_price
            if order_info[0].option2_selectNum == 2:
                option2_name = order_info[0].prd.option2
                option2_price = order_info[0].prd.option2_price
            if order_info[0].option3_selectNum == 2:
                option3_name = order_info[0].prd.option3
                option3_price = order_info[0].prd.option3_price

            refund_price = int(order_info[0].prd.price) + int(option1_price) + int(option2_price) + int(option3_price)

            refund_req = refundTB(user_name=pay_info[0].pay_user.regi_name, user_email=user_id, user_number=pay_info[0].pay_user.regi_phone, pay_num=pay_info[0].pay_num,
                                  prd_title=order_info[0].prd.title, prd_price=order_info[0].prd.price,
                                  option1=option1_name, option1_price=option1_price,
                                  option2=option2_name, option2_price=option2_price,
                                  option3=option3_name, option3_price=option3_price,
                                  prd_total_price=pay_info[0].prd_total_price, refund_price=refund_price,
                                  delivery_price=pay_info[0].delivery_price, delivery_name=pay_info[0].delivery_name,
                                  delivery_addr=pay_info[0].delivery_addr, delivery_phone=pay_info[0].delivery_phone,
                                  delivery_time=pay_info[0].delivery_time, pay_time=pay_info[0].pay_time, pay_way=pay_info[0].payWay.value,
                                  payWay_name=pay_info[0].payWay_name, payWay_account=account_val, merchant_uid=pay_info[0].merchant_uid,
                                  imp_uid=pay_info[0].imp_uid, card_apply =pay_info[0].card_apply)
            refund_req.save()

    return mypage_order_detail(request)


def mypage_profile_modify_addr(request):
    user_id = request.session.get('user_id')
    add01 = request.POST['regi_add01']
    add02 = request.POST['regi_add02']
    add03 = request.POST['regi_add03']

    session = request.session.get('client_id')

    stat_menu_step(request, "myprofile", "modify_addr", add01 + "||" + add02 + "||" + add03)

    if checkSession(session, user_id):
        update_user_addr(user_id, add01, add02, add03)

        user_info = select_register(user_id)
        context = {
            "user_detail": user_info,
            "imp": imp_id,
        }
        return render(request, 'mypage/myprofile.html', context)
    else:
        disableSession(user_id, request)
        context = {
            "msg": message_no_login,
        }
        return render(request, 'login/login.html', context)

def mypage_profile_modify_addr2(request):
    user_id = request.session.get('user_id')
    receiver2_name = request.POST['regi_receiver2_name']
    receiver2_phone = request.POST['regi_receiver2_phone']
    receiver2_add01 = request.POST['regi_receiver2_add01']
    receiver2_add02 = request.POST['regi_receiver2_add02']
    receiver2_add03 = request.POST['regi_receiver2_add03']

    session = request.session.get('client_id')

    stat_menu_step(request, "myprofile", "modify_addr2||" + receiver2_name, receiver2_add01 + "||" + receiver2_add02 + "||" + receiver2_add03 + "||" + receiver2_phone)

    if checkSession(session, user_id):
        update_user_addr2(user_id, receiver2_name,  receiver2_phone, receiver2_add01, receiver2_add02, receiver2_add03)

        user_info = select_register(user_id)
        context = {
            "user_detail": user_info,
            "imp": imp_id,
        }
        return render(request, 'mypage/myprofile.html', context)
    else:
        disableSession(user_id, request)
        context = {
            "msg": message_no_login,
        }
        return render(request, 'login/login.html', context)

def mypage_profile_modify_pw(request):
    user_id = request.session.get('user_id')
    beforePW = request.POST['beforePW']
    newPW = request.POST['newPW']
    session = request.session.get('client_id')

    stat_menu_step(request, "myprofile", "modify_pw" ,"")

    if checkSession(session, user_id):
        user_info = select_register(user_id)
        if user_info.count() is not 0:
            check_pass = bcrypt.checkpw(beforePW.encode('utf-8'), user_info[0].regi_pass.encode('utf-8'))
            if check_pass: #true이면 비번 정보 변경
                new_user = user_info[0]
                password_encrypt = bcrypt.hashpw(newPW.encode('utf-8'), bcrypt.gensalt())
                new_user.regi_pass = password_encrypt.decode('utf-8')
                new_user.save()

                delete_login(user_id)
                request.session['client_id'] = ''
                return render(request, 'login/login.html')

            else: #입력한 기존 비밀번호가 틀리면 error 처리
                context = {
                    "user_detail": user_info,
                    "message": message_diff_pass,
                    "imp": imp_id,
                }

                return render(request, 'mypage/myprofile.html', context)
    else:
        disableSession(user_id, request)
        context = {
            "msg": message_no_login,
        }
        return render(request, 'login/login.html', context)

def mypage_coupon_list(request):
    user_id = request.session.get('user_id')
    session = request.session.get('client_id')

    stat_menu_step(request, "myprofile", "coupon_list", "")

    if checkSession(session, user_id):
        myCoupon_info = select_myCoupon(user_id)
        context = {
            "coupon_detail": myCoupon_info,
        }
        return render(request, 'mypage/mycoupon.html', context)
    else:
        disableSession(user_id, request)
        context = {
            "msg": message_no_login,
        }
        return render(request, 'login/login.html', context)

def mypage_add_coupon(request):
    user_id = request.session.get('user_id')
    coupon_num = request.POST['add_coupon_num']
    session = request.session.get('client_id')

    stat_menu_step(request, "myprofile", "coupon_add", coupon_num)

    if checkSession(session, user_id):
        add_coupon_info = select_coupon_all(coupon_num)
        if add_coupon_info.count() == 1:
            if add_coupon_info[0].dbstat == 'A':
                coupon_user = select_myCoupon_couponNum(user_id, coupon_num)

                if coupon_user.count() > 0:
                    message = message_coupon_already_used
                else:
                    user_info = select_register(user_id)
                    
                    if add_coupon_info[0].coupon_type == 100:
                        #강의실 열어
                        item_info = select_item_group(add_coupon_info[0].prd.prd_code)
                        period = add_coupon_info[0].prd.period * 30
                        expireTime = timezone.now() + timezone.timedelta(days=period)
                        for item in item_info:
                            myclass_list_info = MyClassListTB(user_id=user_id, prd=add_coupon_info[0].prd, pay_num=add_coupon_info[0].coupon_num,
                                                              item_code=item['item_code'],
                                                              expire_time=expireTime, dbstat='A')

                            myclass_list_info.save()

                            my_addCoupon = myCouponTB(user=user_info[0], coupon=add_coupon_info[0], used=True, expire= timezone.now())
                            my_addCoupon.save()
                    else:
                        period = add_coupon_info[0].period * 30  # preiod * 개월(30)
                        expireTime = timezone.now() + timezone.timedelta(days=period)

                        my_addCoupon = myCouponTB(user=user_info[0],coupon=add_coupon_info[0],expire=expireTime)
                        my_addCoupon.save()

                    message = message_coupon_ok
            else:
                message = message_coupon_expired
        else:
            message = message_coupon_diff

        myCoupon_info = select_myCoupon(user_id)
        context = {
            "coupon_detail": myCoupon_info,
            "message": message,
        }
        return render(request, 'mypage/mycoupon.html', context)

    else:
        disableSession(user_id, request)
        context = {
            "msg": message_no_login,
        }
        return render(request, 'login/login.html', context)

