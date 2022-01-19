from django.http import HttpResponse
from django.shortcuts import render
from main.query import *
from main.models import *
from main.codeView.stat import stat_menu_step

import os
import bcrypt


message_ok = 200
message_diff_pass = 202
message_no_regi = 204
message_exist_id = 208
message_wrong_id = 300

def register_page(request):
    return render(request, 'login/register.html')

def check_id_popup(request):
    regi_email = request.POST['regi_email']
    if len(regi_email) > 50:
        stat_menu_step(request, "register popup", "wrong length", regi_email)
        msg = message_exist_id
    else:
        regi_info = select_register_all(regi_email)
        if regi_info.count() is not 0:
            msg = message_exist_id
        else:
            msg = message_ok

    return HttpResponse(msg)

# id로 검색해서 없으면 진행...있으면 에러리턴.
def UserRegister(request):
    regi_email = request.POST['regi_email']


    if len(regi_email) > 50:
        stat_menu_step(request, "register", "wrong length", regi_email)
        return render(request, 'login/login.html')

    val = "admin" in regi_email
    if val:
        stat_menu_step(request, "register", "cant use word", regi_email)
        return render(request, 'login/login.html')

    regi_info = select_register_all(regi_email)  # 회원가입 요청한 ID 가입자 아님을 더블체크


    if regi_info.count() is 0:
        password = request.POST['regi_pass']
        phone_str = request.POST['regi_phone']
        if phone_str.isdigit():
            phone = changePhone_format(request.POST['regi_phone'])
        else:
            stat_menu_step(request, "register", "wrong phone number", phone_str)
            return render(request, 'login/login.html')

        password_encrypt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        stat_menu_step(request, "register", "try", regi_email + "||" + phone)

        regi_new = RegisterTB(regi_email=request.POST['regi_email'], regi_name=request.POST['regi_name'],
                       regi_phone=phone, regi_pass=password_encrypt.decode('utf-8'))
        regi_new.save()

        #메일전송
        return render(request, 'login/login.html')  # 로그인페이지호출
    else:
        return render(request, 'login/login.html')  # register page에서 메시지 출력 이미 가입자입니다.

