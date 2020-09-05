from django.http import HttpResponse
from django.shortcuts import render
from main.query import *
from main.models import *
import bcrypt


message_ok = 200
message_diff_pass = 202
message_no_regi = 204
message_exist_id = 208

def register_page(request):
    return render(request, 'login/register.html')

def check_id_popup(request):
    regi_email = request.POST['regi_email']
    regi_info = select_register_all(regi_email)
    if regi_info.count() is not 0:
        msg = message_exist_id
    else:
        msg = message_ok

    return HttpResponse(msg)

# id로 검색해서 없으면 진행...있으면 에러리턴.
def UserRegister(request):
    regi_email = request.POST['regi_email']
    regi_info = select_register_all(regi_email)  # 회원가입 요청한 ID 가입자 아님을 더블체크

    if regi_info.count() is 0:
        password = request.POST['regi_pass']
        password_encrypt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        regi_new = RegisterTB(regi_email=request.POST['regi_email'], regi_name=request.POST['regi_name'],
                       regi_phone=request.POST['regi_phone'],
                       regi_add01=request.POST['regi_add01'], regi_add02=request.POST['regi_add02'],
                       regi_add03=request.POST['regi_add03'], regi_pass=password_encrypt.decode('utf-8'))
        regi_new.save()
        return render(request, 'login/login.html')  # 로그인페이지호출
    else:
        return HttpResponse(message_exist_id)  # register page에서 메시지 출력 이미 가입자입니다.

