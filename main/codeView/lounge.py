from django.shortcuts import render
from main.query import *
from main.models import *
from main.codeView.stat import stat_menu_step

page_cnt = 6 # display count 노출되는 리스트 갯수

def lounge_page(request):
    category_info = select_lounge_categoy()

    lounge_info = select_lounge()
    total = lounge_info.count()  # use paging

    last_page = int(total) / page_cnt
    reamin = int(total) % page_cnt

    if reamin > 0:
        last_page = int(last_page) + 1

    start_cnt = 0
    end_cnt = start_cnt + page_cnt

    lounge_info_paging = select_lounge_cnt(start_cnt, end_cnt)

    stat_menu_step(request, "coding_lounge", "", "")

    context = {
        "lounge_list": lounge_info_paging,
        "category_list" : category_info,
        "current_category" : 0,
         "last_page": int(last_page),
        "paging_num":1,
        "page_cnt":page_cnt,
        "total_count": total,
    }
    return render(request, 'lounge/coding_lounge.html', context)


def lounge_page_paging(request):
    lounge_all_cnt = request.POST['lounge_all_cnt']  # payInfo total count
    paging_num = int(request.POST['paging_num'])  # 옮기고자 하는 paging 번호
    keyword = request.POST['search_input']

    if lounge_all_cnt == 0:
        lounge_info = select_lounge_search(keyword)
        total = lounge_info.count()  # use paging
    else:
        total = lounge_all_cnt

    start_cnt = 0
    end_cnt = 0
    last_page = int(total) / page_cnt
    reamin = int(total) % page_cnt

    if reamin > 0 or int(last_page) == 0:
        last_page = int(last_page) + 1

    for count in range(0, paging_num):
        if paging_num > 1:
            start_cnt = end_cnt
        end_cnt = start_cnt + page_cnt


    lounge_info_paging = select_lounge_search_cnt(keyword, start_cnt, end_cnt)

    stat_menu_step(request, "coding_lounge", "", keyword)

    context = {
        "lounge_list": lounge_info_paging,
        "last_page": int(last_page),
        "paging_num": paging_num,
        "page_cnt": page_cnt,
        "total_count": total,
    }
    return render(request, 'lounge/coding_lounge.html', context)


def loungeView_page(request):
    lounge_video = request.POST.get('lounge_video', 0)
    lounge_info = select_lounge_videoId(lounge_video)

    stat_menu_step(request, "coding_lounge", "lounge_detail", lounge_info[0].title)
    if lounge_info.count() > 0:
        context = {
            "lounge_video": lounge_video,
            "lounge_info":lounge_info,
        }

        return render(request, 'lounge/coding_lounge_view.html', context)

    else:
        return lounge_page(request)


