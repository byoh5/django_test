from django.shortcuts import render
from main.query import *
from main.models import *

def lounge_page(request):
    lounge_info = select_lounge()
    context = {
        "lounge_list": lounge_info,
    }
    return render(request, 'lounge/coding_lounge.html', context)


def loungeView_page(request):
    lounge_video = request.POST['lounge_video']

    context = {
        "lounge_video": lounge_video,
    }

    return render(request, 'lounge/coding_lounge_view.html', context)