from django.shortcuts import render
from main.models import *
from django.http import HttpResponse

def index(request):
    return render(request, 'main/index_runcoding.html')

def register_page(request):
    return render(request, 'login/register.html')

# Create your views here.
def UserRegister(request):
    print("testing.....")

    q = RegisterTB(regid=1, userid='ABB',name='OBY')
    q.save()
    return HttpResponse("OK")