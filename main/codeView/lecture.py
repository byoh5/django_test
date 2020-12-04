from django.shortcuts import render
from main.query import *
imp_id = 'imp08800373'

def class_page(request):
    class_list_info = select_class_list()
    context = {
        "class_list_detail": class_list_info,
    }

    return render(request, 'class/class_list.html', context)

def class_detail_page(request):
    user_id = request.session.get('user_id', '')
    if user_id == '':
        user = "n"
    else:
        user = "y"

    prd_code = request.POST.get('detail_prd_code', 0)
    items_info = select_class_detail(prd_code)
    html_file = ""

    if items_info.count() > 0:
        html_file = "product/" + items_info[0].prd.list + ".html"

        context = {
            "prd_detail": items_info[0].prd,
            "html_file": html_file,
            "imp": imp_id,
            "user":user,
        }

        return render(request, 'class/class_detail.html', context)
    else:
        user_id = request.session.get('user_id')
        if user_id is not None:
            delete_login(user_id)
        request.session['client_id'] = ''
        request.session['user_id'] = ''

        context = {
            "naver": 0,
        }
        return render(request, 'main/index_runcoding.html', context)

def class_detail_page_prd(request):
    prd_code = request.GET.get('prd_code')
    context = {
        "prd_code": prd_code,
    }

    return render(request, 'class/class_store_detail.html', context)

