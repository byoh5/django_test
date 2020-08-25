from django.shortcuts import render, redirect
from main.models import *
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
    request.session['result'] = ""
    return render(request, 'login/register.html')

def trashcn_arduino_page(request):
    return render(request, 'lecture/lecture_view_arduino.html')

def login_page(request):
    return render(request, 'login/login.html')

def popup_page(request):
    return render(request, 'popup/popup.html')

# 이후 세션 단계로 관리. fix된 url로 들어왔을 때 막기 위함.
def order_page(request):
    session = request.session.get('client_id')
    print(session)

    response_data = {}
    response_data['result'] = 'fail'
    if session is None:
        return HttpResponse(json.dumps(response_data), content_type="application/json") #render(request, 'login/login.html')
    else:
        return render(request, 'payment/order.html') #templete에 없으면 호출이 안됨. ajax

# Create your views here.
def UserRegister(request):

    password = request.POST['regi_pass']
    password_encrypt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    print(password_encrypt);

    q = RegisterTB(regi_id=request.POST['regi_id'], regi_name=request.POST['regi_name'],
                   regi_phone=request.POST['regi_phone'],regi_email=request.POST['regi_email'],
                   regi_add01=request.POST['regi_add01'],regi_add02=request.POST['regi_add02'],
                   regi_add03=request.POST['regi_add03'],regi_pass=password_encrypt.decode('utf-8'))
    q.save()
    return render(request, 'login/login.html') #로그인페이지호출

def login(request):
    response_data = {}

    if request.method == "POST":
        regi_info = RegisterTB.objects.get(regi_id=request.POST['login_id'])

        if regi_info is not None:
            password_encrypt = regi_info.regi_pass # db select
            login_password = request.POST['login_pass']

            check_pass = bcrypt.checkpw(login_password.encode('utf-8'),  password_encrypt.encode('utf-8'))
            print(check_pass) # true/false

            if (check_pass):
                sesseion_auth = bcrypt.hashpw(regi_info.regi_id.encode('utf-8'), bcrypt.gensalt())
                session = sesseion_auth.decode('utf-8')
                print(session)
                request.session['client_id'] = session  # session_auth를 디비에 저장
                request.session['user_id'] = regi_info.regi_id
                # 읽을 떄 client_id = request.session.get('client_id')
                response_data['result'] = 'success'
                return render(request, 'main/index_runcoding.html')
            else:
                response_data['result'] = 'fail'
                response_data['client_id'] = ''
                return render(request, 'login/login.html')

        #return HttpResponse(json.dumps(response_data), content_type="application/json")

        #return render(request, 'contact_form.html', {'form': form})



def logout(request):
    request.session['client_id'] = ''
    request.session['user_id'] = ''
    return render(request, 'main/index_runcoding.html')


def popup(request):
    print("come popup")

    print(request.POST['popup_regiId']);

    try:
        RegisterTB.objects.get(regi_id=request.POST['popup_regiId'])
        print("Exist.....")
        request.session['result'] = 'exist'
        return render(request, 'popup/popup.html')
    except:
        print("DoesNotExist.....")
        request.session['result'] = 'ok'
        return render(request, 'popup/popup.html')



