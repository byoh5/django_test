from django.shortcuts import render
from main.query import *
from main.models import *

def class_page(request):
    class_list_info = select_class_list()
    context = {
        "class_list_detail": class_list_info,
    }

    return render(request, 'class/class_list.html', context)

def class_detail_page(request):
    prd_code = request.POST['detail_prd_code']
    items_info = select_class_detail(prd_code)

    context = {
        "class_items_detail": items_info,
        "prd_detail": items_info[0].prd,
    }

    return render(request, 'class/class_detail.html', context)