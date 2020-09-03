from django.shortcuts import render
from main.query import *
from main.models import *
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
            password_encrypt = regi_info[0].regi_pass
            regi_id = regi_info[0].regi_id
            login_password = request.POST['login_pass']
            check_pass = bcrypt.checkpw(login_password.encode('utf-8'), password_encrypt.encode('utf-8'))
            if check_pass:
                session_auth = bcrypt.hashpw(regi_id.encode('utf-8'), bcrypt.gensalt())
                session = session_auth.decode('utf-8')
                delete_login(login_id) # 기존에 로그인 한 정보가 있다면 지움.

                q = LoginTB(user_id=login_id, session_id=session) #새로운 로그인 정보 등록
                q.save()

                request.session['client_id'] = session #쿠기에 정보 저장
                request.session['user_id'] = regi_id
                request.session['result'] = 'success'
                request.session.modified = True
                context = {
                    "client_id": session,
                    "user_id": regi_id,
                    "result": message_ok,
                }
                return render(request, 'main/index_runcoding.html', context)
            else:
                request.session['result'] = message_diff_pass
                request.session['client_id'] = ''
                context = {
                    "client_id": '',
                    "user_id": regi_id,
                    "result": message_diff_pass,
                }
                return render(request, 'login/login.html', context)
        else:
            request.session['result'] = message_no_regi
            request.session['client_id'] = ''
            context = {
                "client_id": '',
                "user_id": '',
                "result": message_no_regi,
            }
            return render(request, 'login/login.html', context)  # 가입자가 아닙니다.


def logout(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        delete_login(user_id)
    request.session['client_id'] = ''
    return render(request, 'main/index_runcoding.html')

