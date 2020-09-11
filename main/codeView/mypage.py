from django.shortcuts import render
from main.query import *
from main.models import *
import bcrypt

def mypage_profile(request):
    user_id = request.session.get('user_id')
    user_info = select_register(user_id)
    context = {
        "user_detail": user_info,
    }
    return render(request, 'mypage/myprofile.html', context)

def mypage_order(request):
    user_id = request.session.get('user_id')
    pay_user_info = select_pay_user(user_id)
    context = {
        "user_detail": pay_user_info,
    }
    return render(request, 'mypage/myorder.html', context)

def mypage_order_detail(request):
    pay_idx = request.POST['pay_idx']
    pay_info = select_pay(pay_idx)
    print(pay_info[0].pay_num)
    context = {
        "pay_detail": pay_info,
    }
    return render(request, 'mypage/myorder_detail.html', context)

def mypage_profile_modify_addr(request):
    user_id = request.session.get('user_id')
    name = request.POST['regi_receiver1_name']
    add01 = request.POST['regi_add01']
    add02 = request.POST['regi_add02']
    add03 = request.POST['regi_add03']

    update_user_addr(user_id, name, add01, add02, add03)

    user_info = select_register(user_id)
    context = {
        "user_detail": user_info,
    }
    return render(request, 'mypage/myprofile.html', context)

def mypage_profile_modify_addr2(request):
    user_id = request.session.get('user_id')
    receiver2_name = request.POST['regi_receiver2_name']
    receiver2_phone = request.POST['regi_receiver2_phone']
    receiver2_add01 = request.POST['regi_receiver2_add01']
    receiver2_add02 = request.POST['regi_receiver2_add02']
    receiver2_add03 = request.POST['regi_receiver2_add03']

    update_user_addr2(user_id, receiver2_name,  receiver2_phone, receiver2_add01, receiver2_add02, receiver2_add03)

    user_info = select_register(user_id)
    context = {
        "user_detail": user_info,
    }
    return render(request, 'mypage/myprofile.html', context)

def mypage_profile_modify_pw(request):
    user_id = request.session.get('user_id')
    beforePW = request.POST['beforePW']
    newPW = request.POST['newPW']

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
            }

            return render(request, 'mypage/myprofile.html', context)

