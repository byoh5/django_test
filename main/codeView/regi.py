from django.shortcuts import render
from main.query import *
from main.models import *
import bcrypt

def register_page(request):
    return render(request, 'login/register.html')

def check_id_popup(request):
    regi_id = request.POST['popup_regiId']
    regi_info = select_register(regi_id)
    if regi_info.count() is not 0:
        context = {
            "popup_message": message_exist_id,  # 전역 변수로 변경 필요
            "regiId":regi_id,
        }
    else:
        context = {
            "popup_message": message_ok,
            "regiId": regi_id,
        }

    return render(request, 'login/register.html', context)




# id로 검색해서 없으면 진행...있으면 에러리턴.
def UserRegister(request):
    regi_id = request.POST['regi_id']
    regi_info = select_register(regi_id)  # 회원가입 요청한 ID 가입자 아님을 더블체크

    if regi_info.count() is 0:
        password = request.POST['regi_pass']
        password_encrypt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        q = RegisterTB(regi_id=regi_id, regi_name=request.POST['regi_name'],
                       regi_phone=request.POST['regi_phone'], regi_email=request.POST['regi_email'],
                       regi_add01=request.POST['regi_add01'], regi_add02=request.POST['regi_add02'],
                       regi_add03=request.POST['regi_add03'], regi_pass=password_encrypt.decode('utf-8'))
        q.save()
        return render(request, 'login/login.html')  # 로그인페이지호출
    else:
        context = {
            "popup_message": message_exist_id,
            "regiId": regi_id,
        }
        return render(request, 'login/register.html', context)  # register page에서 메시지 출력 이미 가입자입니다.

