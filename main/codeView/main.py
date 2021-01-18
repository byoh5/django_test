from django.shortcuts import render
from main.query import *


def main_page(request):
    popup_active = select_poopup_active()
    context = {
        "naver": 0,
        "popup_cnt": popup_active.count(),
    }
    return render(request, 'main/index_runcoding.html', context)

def main_naver_page(request):
    context = {
        "naver": 1,
    }
    return render(request, 'main/index_runcoding.html', context)

def popup_page(request):
    print("come")
    # popup_active = select_poopup_active()
    # context = {
    #     "popup": popup_active,
    # }
    return render(request, 'popup/popup.html')