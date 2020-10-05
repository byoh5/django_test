from django.shortcuts import render
from main.query import *
from main.models import *
import bcrypt

message_ok = 200
message_diff_pass = 202
message_no_regi = 204
message_exist_id = 208

message_coupon_ok = 300
message_coupon_diff = 302
message_coupon_expired = 304
message_coupon_already_used = 306
imp_id = 'imp08800373'

def mypage_profile(request):
    user_id = request.session.get('user_id')
    session = request.session.get('client_id')

    if checkSession(session, user_id):
        user_info = select_register(user_id)
        context = {
            "user_detail": user_info,
            "imp": imp_id,
        }
        return render(request, 'mypage/myprofile.html', context)
    else:
        return disableSession(user_id, request)


def mypage_order(request):
    user_id = request.session.get('user_id')
    session = request.session.get('client_id')

    if checkSession(session, user_id):
        pay_user_info = select_pay_user(user_id)
        context = {
            "user_detail": pay_user_info,
        }
        return render(request, 'mypage/myorder.html', context)
    else:
        return disableSession(user_id, request)

def mypage_order_detail(request):
    pay_idx = request.POST['pay_idx']
    user_id = request.session.get('user_id')
    session = request.session.get('client_id')

    if checkSession(session, user_id):
        pay_info = select_pay(pay_idx)
        mycoupon_name = ""
        option_name = ""

        if pay_info[0].coupon_num != "" :
            mycoupon_info = select_myCoupon_couponNum(user_id, pay_info[0].coupon_num)
            if mycoupon_info.count() > 0:
                mycoupon_name = mycoupon_info[0].coupon.coupon_name

        split_order = pay_info[0].order_id.split(',')
        # product -> myclass에 넣고, 장바구니 정리하기
        for data in split_order:
            if len(data) > 0:
                order_info = select_order_info(data, user_id)
                if order_info.count() > 0:
                    if order_info[0].option1_selectNum == 2:
                        option_name += order_info[0].prd.option1

                    if order_info[0].option2_selectNum == 2:
                        if option_name != "":
                            option_name += ","
                        option_name += order_info[0].prd.option2

                    if order_info[0].option3_selectNum == 2:
                        if option_name != "":
                            option_name += ","
                        option_name += order_info[0].prd.option3

        context = {
            "pay_detail": pay_info,
            "mycoupon_name": mycoupon_name,
            "option":option_name,
        }
        return render(request, 'mypage/myorder_detail.html', context)
    else:
        return disableSession(user_id, request)


def mypage_profile_modify_addr(request):
    user_id = request.session.get('user_id')
    name = request.POST['regi_receiver1_name']
    add01 = request.POST['regi_add01']
    add02 = request.POST['regi_add02']
    add03 = request.POST['regi_add03']

    session = request.session.get('client_id')

    if checkSession(session, user_id):
        update_user_addr(user_id, name, add01, add02, add03)

        user_info = select_register(user_id)
        context = {
            "user_detail": user_info,
            "imp": imp_id,
        }
        return render(request, 'mypage/myprofile.html', context)
    else:
        return disableSession(user_id, request)

def mypage_profile_modify_addr2(request):
    user_id = request.session.get('user_id')
    receiver2_name = request.POST['regi_receiver2_name']
    receiver2_phone = request.POST['regi_receiver2_phone']
    receiver2_add01 = request.POST['regi_receiver2_add01']
    receiver2_add02 = request.POST['regi_receiver2_add02']
    receiver2_add03 = request.POST['regi_receiver2_add03']

    session = request.session.get('client_id')

    if checkSession(session, user_id):
        update_user_addr2(user_id, receiver2_name,  receiver2_phone, receiver2_add01, receiver2_add02, receiver2_add03)

        user_info = select_register(user_id)
        context = {
            "user_detail": user_info,
            "imp": imp_id,
        }
        return render(request, 'mypage/myprofile.html', context)
    else:
        return disableSession(user_id, request)

def mypage_profile_modify_pw(request):
    user_id = request.session.get('user_id')
    beforePW = request.POST['beforePW']
    newPW = request.POST['newPW']
    session = request.session.get('client_id')

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
        return disableSession(user_id, request)

def mypage_coupon_list(request):
    user_id = request.session.get('user_id')
    session = request.session.get('client_id')

    if checkSession(session, user_id):
        myCoupon_info = select_myCoupon(user_id)
        context = {
            "coupon_detail": myCoupon_info,
        }
        return render(request, 'mypage/mycoupon.html', context)
    else:
        return disableSession(user_id, request)

def mypage_add_coupon(request):
    user_id = request.session.get('user_id')
    coupon_num = request.POST['add_coupon_num']
    session = request.session.get('client_id')

    if checkSession(session, user_id):
        add_coupon_info = select_coupon_all(coupon_num)
        if add_coupon_info.count() == 1:
            if add_coupon_info[0].dbstat == 'A':
                coupon_user = select_myCoupon_couponNum(user_id, coupon_num)

                if coupon_user.count() > 0:
                    message = message_coupon_already_used
                else:
                    user_info = select_register(user_id)

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
        return disableSession(user_id, request)