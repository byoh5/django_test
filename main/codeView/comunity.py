from django.shortcuts import render
from main.query import *
from main.models import *


def comunity_page(request):
    return render(request, 'comunity/coding_comunity.html')

