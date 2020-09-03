from django.shortcuts import render
from main.query import *
from main.models import *

def lounge_page(request):
    return render(request, 'lounge/coding_lounge.html')


def loungeView_page(request):
    return render(request, 'lounge/coding_lounge_view.html')