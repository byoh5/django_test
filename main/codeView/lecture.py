from django.shortcuts import render
from main.query import *

from main.codeView.stat import stat_menu_step

imp_id = 'imp08800373'

def class_page(request):
    class_list_info = select_class_list()
    category_large = select_class_category_lar_list()

    stat_menu_step(request,"codingkit_list", "", "")

    context = {
        "class_list_detail": class_list_info,
        "category_large": category_large,
        "total_count": class_list_info.count(),
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
    print(prd_code)
    html_file = ""

    if items_info.count() > 0:
        html_file = "product/" + items_info[0].prd.list + ".html"

        stat_menu_step(request, "codingkit_detail", items_info[0].prd.keyword + "(" + prd_code + ") ||" + html_file, "")

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

