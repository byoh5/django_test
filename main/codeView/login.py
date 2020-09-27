from django.http import HttpResponse
from django.shortcuts import render, redirect
from main.query import *
from main.models import *
from main.codeView.email import *
import bcrypt


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

                order_info = select_order(login_id)

                request.session['client_id'] = session #쿠기에 정보 저장
                request.session['order_count'] = order_info.count()
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

