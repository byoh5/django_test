from django.shortcuts import render
from main.models import *
from django.http import HttpResponse
import bcrypt

import json
from django.http import HttpResponse

def index(request):
    return render(request, 'main/index_runcoding.html')

def register_page(request):
    return render(request, 'login/register.html')

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

def idChecker(request):
    response_data = {}

    try:
        RegisterTB.objects.get(regi_id=request.POST['regi_id'])
        print("Exist.....")
        response_data['result'] = 'exist'
    except:
        print("DoesNotExist.....")
        response_data['result'] = 'success'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def login_page(request):
    return render(request, 'login/login.html')

def login(request):
    response_data = {}
    regi_info = RegisterTB.objects.get(regi_id=request.POST['login_id'])

    password_encrypt = regi_info.regi_pass
    print(password_encrypt) # db select

    login_password = request.POST['login_pass']

    check_pass = bcrypt.checkpw(login_password.encode('utf-8'),  password_encrypt.encode('utf-8'))
    print(check_pass)

    if(check_pass):
        response_data['result'] = 'true'
    else:
        response_data['result'] = 'fail'

    # csrf 토근을 이용해서 cookies를 지정하면 될듯

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def order_page(request):
    return render(request, 'payment/order.html')
