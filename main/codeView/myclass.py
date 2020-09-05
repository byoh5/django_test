from django.shortcuts import render
from main.query import *
from main.models import *

def myclass_list_page(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        myclass_list_info = select_myclass_list(user_id)

        context = {
            "myclass_list_detail": myclass_list_info,
        }
        return render(request, 'myclass/myclass_list.html', context)
    return render(request, 'myclass/myclass_list.html')


def myclass_page(request):
    prdCode = request.POST['prdCode']

    item_info = select_class_detail(prdCode)
    downdata_info = select_downdata(prdCode)

    if item_info.count() is not 0:
        context = {
            "myclass_detail": item_info,
            "title": item_info[0].prd.title2,
            "sub_title": item_info[0].prd.title3,
            "downData": downdata_info,
        }
        return render(request, 'myclass/myclass.html', context)
