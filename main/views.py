from django.shortcuts import render, redirect
from django.utils import timezone
from main.models import *
from datetime import datetime
import bcrypt

import json
from django.http import HttpResponse
from django.db import models
#RegisterTB 테이블 import 확인하기

def index(request):
    return render(request, 'main/index_runcoding.html')

def index_page(request):
    return render(request, 'main/index.html')

def register_page(request):
    request.session['IDresult'] = ""
    return render(request, 'login/register.html')

def login_page(request):
    return render(request, 'login/login.html')

def popup_page(request):
    request.session['IDresult'] = ""
    return render(request, 'popup/popup.html')

def class_page(request):
    return render(request, 'class/class_list.html')

def trashcn_arduino_page(request):
    return render(request, 'class/class_view_arduino.html')

def trashcn_mblock_page(request):
    return render(request, 'class/class_view_mblock.html')

def myclass_list_page(request):
    return render(request, 'myclass/myclass_list.html')

def myclass_page(request):
    return render(request, 'myclass/myclass.html')

# 이후 세션 단계로 관리. fix된 url로 들어왔을 때 막기 위함.
def order_page(request):
    session = request.session.get('client_id')
    userid = request.session.get('user_id') #이 값으로 디비에서 정보찾고..
    print(session)


    #구매하는 제품 form의 title # 이값으로 prd_table 뒤져서 가겨계산하고... order table에 insert

    if session is None:
        return render(request, 'lecture/lecture_view_arduino.html')
    else:
        return render(request, 'payment/order.html') #templete에 없으면 호출이 안됨. ajax

# Create your views here.
# id로 검색해서 없으면 진행...있으면 에러리턴.
def UserRegister(request):
    regi_info = RegisterTB.objects.filter(regi_id=request.POST['regi_id'], dbstat='A') # 회원가입 요청한 ID 가입자 아님을 더블체크

    if regi_info.count() is 0:
        password = request.POST['regi_pass']
        password_encrypt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
        print(password_encrypt);
    
        q = RegisterTB(regi_id=request.POST['regi_id'], regi_name=request.POST['regi_name'],
                       regi_phone=request.POST['regi_phone'],regi_email=request.POST['regi_email'],
                       regi_add01=request.POST['regi_add01'],regi_add02=request.POST['regi_add02'],
                       regi_add03=request.POST['regi_add03'],regi_pass=password_encrypt.decode('utf-8'),
                       stime=datetime.now())

        # from datetime import datetime
        # from django.utils import timezone
        # date_str = "2016-02-20 15:03:55"
        # v = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

        q.save()
        return render(request, 'login/login.html') #로그인페이지호출
    else:
        return render(request, 'login/register.html') #register page에서 메시지 출력 이미 가입자입니다.

def login(request):
    if request.method == "POST":
        loginId = request.POST['login_id']
        regi_info = RegisterTB.objects.filter(regi_id=loginId, dbstat='A')

        #debug용 - 지우지 마시오
        #print(regi_info.count())
        #print(str(regi_info.query))
        #print(regi_info)
        #print(regi_info[0].regi_pass)

        if regi_info.count() is not 0:
            password_encrypt = regi_info[0].regi_pass # db select
            regi_id = regi_info[0].regi_id
            login_password = request.POST['login_pass']

            check_pass = bcrypt.checkpw(login_password.encode('utf-8'),  password_encrypt.encode('utf-8'))
            print(check_pass) # true/false

            if (check_pass): # 비밀번호가 맞으면 login table에 저장
                session_auth = bcrypt.hashpw(regi_id.encode('utf-8'), bcrypt.gensalt())
                session = session_auth.decode('utf-8')

                q = LoginTB(user_id=loginId, session_id=session, login_time=datetime.now())
                q.save()

                request.session['client_id'] = session  # session_auth를 디비에 저장
                request.session['user_id'] = regi_id
                # 읽을 때 client_id = request.session.get('client_id')
                request.session['result'] = 'success'
                return render(request, 'main/index_runcoding.html')

            else:  # 비밀번호가 틀리면
                request.session['result'] = 'fail'
                request.session['client_id'] = ''
                return render(request, 'login/login.html')

        else:  # 로그인 ID가 가입자가 아니면
            request.session['result'] = 'fail'
            request.session['client_id'] = ''
            return render(request, 'login/login.html')  #가입자가 아닙니다.

def logout(request):
    user_id = request.session.get('user_id')
    login_info = LoginTB.objects.filter(user_id=user_id, dbstat='A')
    print(user_id)
    print(login_info.count())
    
    if login_info.count() is not 0:
        login_info[0].dbstat = 'D-'
        login_info[0].logout_time = datetime.now()
        login_info[0].save()

    request.session['client_id'] = ''
    request.session['user_id'] = ''
    return render(request, 'main/index_runcoding.html')


def popup(request):
    regi_info = RegisterTB.objects.filter(regi_id=request.POST['popup_regiId'], dbstat='A')
    print(str(regi_info.query))

    print(regi_info.count())

    if regi_info.count() is not 0:
        print("Exist.....")
        request.session['IDresult'] = 'exist'
        return render(request, 'popup/popup.html')
    else:
        print("DoesNotExist.....")
        request.session['IDresult'] = 'ok'
        return render(request, 'popup/popup.html')



