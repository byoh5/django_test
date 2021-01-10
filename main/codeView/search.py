from django.shortcuts import render
from main.query import *
from main.models import *
from main.codeView.stat import stat_menu_step

def search_prd(request):
    keyword = request.POST.get('src_inp', 0)
    category_large = request.POST.get('large', 0)

    if keyword == 0 and category_large == 0 :
        search_prd = select_class_list()
        category_large_list = select_class_category_lar_list()
        stat_menu_step(request, "class_list", "", "")
        context = {
            "class_list_detail": search_prd,
            "category_large": category_large_list,
            "total_count": search_prd.count(),
        }
        return render(request, 'class/class_list.html', context)
    else:
        search_prd = select_prd_category_search(category_large, keyword)

        category_large_list = select_class_category_lar_list()
        stat_menu_step(request, "class_list", "", category_large + " || " + keyword)
        context = {
            "class_list_detail": search_prd,
            "select_large":category_large,
            "category_large": category_large_list,
            "total_count": search_prd.count(),
        }
        return render(request, 'class/class_list.html', context)
