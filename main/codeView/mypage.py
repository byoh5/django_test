from django.shortcuts import render
from main.query import *
from main.models import *

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

def mypage_profile_modify_addr(request):
    user_id = request.session.get('user_id')
    add01 = request.POST['regi_add01']
    add02 = request.POST['regi_add02']
    add03 = request.POST['regi_add03']
    update_user_addr(user_id, add01, add02, add03)

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

