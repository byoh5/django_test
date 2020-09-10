from django.shortcuts import render
from main.query import *
from main.models import *


def comunity_page(request):
    comunity_info = select_comunity()
    category_info = select_category()
    context = {
        "comunity_list": comunity_info,
        "category_list": category_info,
    }
    return render(request, 'comunity/coding_comunity.html', context)

def comunity_page_category(request):
    category_idx = request.POST['category_idx']
    print(category_idx)