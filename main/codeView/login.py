from django.http import HttpResponse
from django.shortcuts import render, redirect
from main.query import *
from main.models import *
from main.codeView.email import *
import bcrypt
import string
import random

message_ok = 200
message_diff_pass = 202
message_no_regi = 204
message_exist_id = 208

def login_page(request):
    return render(request, 'login/login.html')

def naverLogin_page(request):
    return render(request, 'login/naverlogin.html')

def login(request):
    if request.method == "POST":
        login_id = request.POST['login_id']
        regi_info = select_register(login_id)
        if regi_info.count() is not 0:
            email = regi_info[0].regi_email

            password_encrypt = regi_info[0].regi_pass
            login_password = request.POST['login_pass']
            check_pass = bcrypt.checkpw(login_password.encode('utf-8'), password_encrypt.encode('utf-8'))

            if check_pass:
                session_auth = bcrypt.hashpw(email.encode('utf-8'), bcrypt.gensalt())
                session = session_auth.decode('utf-8')
                delete_login(login_id) # 기존에 로그인 한 정보가 있다면 지움.

                q = LoginTB(user_id=login_id, session_id=session) #새로운 로그인 정보 등록
                q.save()

                request.session['client_id'] = session #쿠기에 정보 저장
                request.session['user_id'] = login_id
                return HttpResponse(message_ok)
            else:
                return HttpResponse(message_diff_pass)
        else:
            return HttpResponse(message_no_regi) # 가입자가 아닙니다.


def logout(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        delete_login(user_id)
    request.session['client_id'] = ''
    request.session['user_id'] = ''
    return render(request, 'main/index_runcoding.html')

def find_pass_viaEmail(request):
    if request.method == "POST":
        find_loginId = request.POST['find_loginId']
        regi_info = select_register(find_loginId) # 가입자 인지 확인
        if regi_info.count() is 0:
            return HttpResponse(message_no_regi)
        else:
            string_pool = string.ascii_letters
            number_pool = string.digits
            _LENGTH = 6
            newPW = ""
            for i in range(_LENGTH):
                if i == 2 or i == 5:
                    newPW += random.choice(number_pool)
                else:
                    newPW += random.choice(string_pool)  # 랜덤한 문자열 하나 선택
            print(newPW)

            new_user = regi_info[0]
            password_encrypt = bcrypt.hashpw(newPW.encode('utf-8'), bcrypt.gensalt())
            new_user.regi_pass = password_encrypt.decode('utf-8')
            new_user.save()

            result = sendEmail(find_loginId, "런코딩에서 발송된 메일입니다.", "안녕하세요. 런코딩입니다. 임시로 발급된 비밀번호는 [" + newPW + "] 입니다. 빠른시간에 변경 바랍니다.")

            if result == 200:
                return HttpResponse(message_ok)
