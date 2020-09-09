from django.shortcuts import render
from main.query import *
from main.models import *


def comunity_page(request):
    comunity_info = select_comunity()
    context = {
        "comunity_list": comunity_info,
    }
    return render(request, 'comunity/coding_comunity.html', context)

