from django.shortcuts import render
from main.query import *
from main.models import *

def search_prd(request):
    keyword = request.POST['src_inp']
    if keyword == 'all':
        search_prd = select_class_list()
    else:
        search_prd = select_prd_keyword(keyword)
    context = {
        "class_list_detail": search_prd,
    }
    return render(request, 'class/class_list.html', context)
