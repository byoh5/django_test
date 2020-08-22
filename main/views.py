from django.shortcuts import render
from main.models import *
from django.http import HttpResponse

import json
from django.http import HttpResponse

def index(request):
    return render(request, 'main/index_runcoding.html')

def register_page(request):
    return render(request, 'login/register.html')

# Create your views here.
def UserRegister(request):
    print("testing.....")
    try:
        RegisterTB.objects.get(name='OBY1').name
        print("Exist.....")
    except:
        print("DoesNotExist.....")

    print("testing.....")
    q = RegisterTB(regid=1, userid='ABB',name='OBY')
    q.save()
    return HttpResponse("OK")

def idChecker(request):
    response_data = {}

    try:
        RegisterTB.objects.get(userid=request.POST['regi_id']).name
        print("Exist.....")
        response_data['result'] = 'exist'
    except:
        print("DoesNotExist.....")
        response_data['result'] = 'success'

    return HttpResponse(json.dumps(response_data), content_type="application/json")
