from django.shortcuts import render
from main.models import *
from main.query import *


def index(request):
    return render(request, 'main/index_runcoding.html')


