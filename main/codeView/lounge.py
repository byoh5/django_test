from django.shortcuts import render
from main.query import *
from main.models import *

def lounge_page(request):
    lounge_info = select_lounge()
    count = lounge_info.count() # use paging
    category_info = select_lounge_categoy()
    context = {
        "lounge_list": lounge_info,
        "category_list" : category_info,
        "current_category" : 0,
    }
    return render(request, 'lounge/coding_lounge.html', context)


def loungeView_page(request):
    lounge_video = request.POST['lounge_video']

    context = {
        "lounge_video": lounge_video,
    }

    return render(request, 'lounge/coding_lounge_view.html', context)

def search_lounge(request):
    sort = request.POST['sort']
    category = request.POST['category']
    keyword = request.POST['search_input']

    lounge_info = select_lounge_search(sort, category, keyword)
    category_info = select_lounge_categoy()

    context = {
        "lounge_list": lounge_info,
        "category_list": category_info,
        "current_category": category,
    }
    return render(request, 'lounge/coding_lounge.html', context)
