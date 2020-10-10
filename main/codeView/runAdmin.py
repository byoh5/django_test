from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from main.query import *
from main.models import *

from main.codeView.payment import *

pay_status_ok = 1
pay_status_delivery = 2
pay_status_delivery_done = 3
pay_status_prepay = 4
pay_status_deposit_noCheck = 5

message_no_login = 210

display_count = 10

def deposit_list(request):
    return render(request, 'runAdmin/deposit_list.html')

def deposit_search(request):
    userid = request.session.get('user_id')
    user_info = select_register(userid)
    deposit_all_cnt = request.POST['deposit_all_cnt']  # total count
    paging_num = int(request.POST['paging_num'])  # 옮기고자 하는 paging 번호
    page_cnt = display_count  # display count 노출되는 리스트 갯수

    if user_info is not None:
        if user_info[0].level == 100:
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            searchBox = request.POST['searchBox']

            split_start = start_date.split('-')
            start_year = int(split_start[0])
            start_month = int(split_start[1])
            start_day = int(split_start[2])
            start_datetime_filter = datetime(start_year, start_month, start_day)

            split_end = end_date.split('-')
            end_year = int(split_end[0])
            end_month = int(split_end[1])
            end_day = int(split_end[2]) + 1
            end_datetime_filter = datetime(end_year, end_month, end_day)

            if deposit_all_cnt == "":
                pay_info = select_pay_date_deposit(start_datetime_filter, end_datetime_filter, searchBox)
                total = pay_info.count()
            else:
                total = deposit_all_cnt

            start_cnt = 0
            end_cnt = 0
            last_page = int(total) / page_cnt
            reamin = int(total) % page_cnt

            if reamin > 0:
                last_page = int(last_page) + 1

            for count in range(0, paging_num):
                if paging_num > 1:
                    start_cnt = end_cnt
                end_cnt = start_cnt + page_cnt

            new_pay_info = select_pay_date_deposit_paging(start_datetime_filter, end_datetime_filter, searchBox, start_cnt, end_cnt)
            myclass_list_info = select_myclass_date_deposit(start_datetime_filter, end_datetime_filter)

            context = {
                "pay_info": new_pay_info,
                "total_count":total,
                "myclass_list":myclass_list_info,
                "start_date": start_date,
                "end_date": end_date,
                "search": searchBox,
                "last_page": int(last_page),
                "paging_num": paging_num,
            }
            return render(request, 'runAdmin/deposit_list.html', context)
        else:
            disableSession(userid, request)
            context = {
                "msg": message_no_login,
            }
            return render(request, 'login/login.html', context)
    else:
        return render(request, 'login/login.html')

def deposit_change(request):
    pay_num = request.POST['pay_num']
    user_id = request.POST['user_id']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    searchBox = request.POST['searchBox']
    admin = request.session.get('user_id')

    myclass_list_info = select_myclass_list_payNum(user_id, pay_num)
    for myclass_list in myclass_list_info:
        new_myclass_list = myclass_list
        new_myclass_list.dbstat = 'A'
        new_myclass_list.save()

    year = timezone.localtime().year
    month = timezone.localtime().month
    day = timezone.localtime().day

    pay_userStatus_info = select_userStatue(pay_status_ok)
    pay_info = select_pay_user_payNum(user_id, pay_num)
    new_pay = pay_info[0]
    new_pay.pay_user_status = pay_userStatus_info[0]
    new_pay.pay_result = 0
    new_pay.pay_result_info = '입금확인-' + admin + "-"+str(year) + str(month) + str(day)
    new_pay.save()

    split_start = start_date.split('-')
    start_year = int(split_start[0])
    start_month = int(split_start[1])
    start_day = int(split_start[2])
    start_datetime_filter = datetime(start_year, start_month, start_day)

    split_end = end_date.split('-')
    end_year = int(split_end[0])
    end_month = int(split_end[1])
    end_day = int(split_end[2]) + 1
    end_datetime_filter = datetime(end_year, end_month, end_day)

    pay_info = select_pay_date_deposit(start_datetime_filter, end_datetime_filter, searchBox)
    myclass_list_info = select_myclass_date_deposit(start_datetime_filter, end_datetime_filter)

    context = {
        "pay_info": pay_info,
        "total_count": pay_info.count(),
        "myclass_list": myclass_list_info,
        "start_date": start_date,
        "end_date": end_date,
        "search": searchBox,
    }
    return render(request, 'runAdmin/deposit_list.html', context)

def pay_list(request):
    userStatus_info = select_userStatus_all()
    context = {
        "userStatus_info": userStatus_info,
        "page_cnt":'2',
        "status": '0',
    }
    return render(request, 'runAdmin/pay_list.html', context)

def pay_search(request):
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    searchBox = request.POST['searchBox']
    status = request.POST['status']
    pay_all_cnt = request.POST['pay_all_cnt'] #payInfo total count
    paging_num = int(request.POST['paging_num']) #옮기고자 하는 paging 번호
    page_cnt = int(request.POST['page_cnt']) #display count 노출되는 리스트 갯수

    split_start = start_date.split('-')
    start_year = int(split_start[0])
    start_month = int(split_start[1])
    start_day = int(split_start[2])
    start_datetime_filter = datetime(start_year, start_month, start_day)

    split_end = end_date.split('-')
    end_year = int(split_end[0])
    end_month = int(split_end[1])
    end_day = int(split_end[2]) + 1
    end_datetime_filter = datetime(end_year, end_month, end_day)

    if pay_all_cnt == "":
        pay_info = select_pay_date(start_datetime_filter, end_datetime_filter, searchBox, status)
        total = pay_info.count()
    else:
        total = pay_all_cnt

    start_cnt = 0
    end_cnt = 0
    last_page = int(total) / page_cnt
    reamin = int(total) % page_cnt

    if reamin > 0:
        last_page = int(last_page) + 1

    for count in range(0, paging_num):
        if paging_num > 1:
            start_cnt = end_cnt
        end_cnt = start_cnt + page_cnt

    pay_info_paging = select_pay_date_cnt(start_datetime_filter, end_datetime_filter, searchBox, status, start_cnt, end_cnt)
    order_info = select_order_date(start_datetime_filter, end_datetime_filter, searchBox)
    userStatus_info = select_userStatus_all()

    context = {
        "pay_info": pay_info_paging,
        "total_count": total,
        "start_date": start_date,
        "end_date": end_date,
        "order_info": order_info,
        "userStatus_info":userStatus_info,
        "status":status,
        "search": searchBox,
        "ok_status": pay_status_ok,
        "last_page": int(last_page),
        "paging_num":paging_num,
        "page_cnt":page_cnt,
    }

    return render(request, 'runAdmin/pay_list.html', context)

def pay_change(request):
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    searchBox = request.POST['searchBox']
    status = request.POST['status']
    pay_idx = request.POST['pay_idx']
    admin = request.session.get('user_id')

    year = timezone.localtime().year
    month = timezone.localtime().month
    day = timezone.localtime().day

    pay_userStatus_info = select_userStatue(pay_status_delivery)

    split_pay = pay_idx.split(',')

    # product -> myclass에 넣고, 장바구니 정리하기
    for data in split_pay:
        if len(data) > 0:
            pay_info = select_pay(data)
            new_pay = pay_info[0]
            new_pay.pay_user_status = pay_userStatus_info[0]
            new_pay.pay_result_info = '배송중-' + admin + "-" + str(year) + str(month) + str(day)
            new_pay.save()

    split_start = start_date.split('-')
    start_year = int(split_start[0])
    start_month = int(split_start[1])
    start_day = int(split_start[2])
    start_datetime_filter = datetime(start_year, start_month, start_day)

    split_end = end_date.split('-')
    end_year = int(split_end[0])
    end_month = int(split_end[1])
    end_day = int(split_end[2]) + 1
    end_datetime_filter = datetime(end_year, end_month, end_day)

    pay_info = select_pay_date(start_datetime_filter, end_datetime_filter, searchBox, status)
    order_info = select_order_date(start_datetime_filter, end_datetime_filter, searchBox)
    userStatus_info = select_userStatus_all()
    context = {
        "pay_info": pay_info,
        "total_count": pay_info.count(),
        "start_date": start_date,
        "end_date": end_date,
        "order_info": order_info,
        "userStatus_info": userStatus_info,
        "status": status,
        "search": searchBox,
        "ok_status":pay_status_ok,
    }

    return render(request, 'runAdmin/pay_list.html', context)

def user_list(request):
    context = {
        "page_cnt": '2',
        "status": '0',
    }
    return render(request, 'runAdmin/user_list.html', context)

def user_search(request):
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    user_id = request.POST['searchBox']
    user_all_cnt = request.POST['user_all_cnt'] #payInfo total count
    paging_num = int(request.POST['paging_num']) #옮기고자 하는 paging 번호
    page_cnt = display_count #display count 노출되는 리스트 갯수

    start_datetime_filter = ""
    end_datetime_filter = ""

    if start_date is not "":
        split_start = start_date.split('-')
        start_year = int(split_start[0])
        start_month = int(split_start[1])
        start_day = int(split_start[2])
        start_datetime_filter = datetime(start_year, start_month, start_day)

    if end_date is not "":
        split_end = end_date.split('-')
        end_year = int(split_end[0])
        end_month = int(split_end[1])
        end_day = int(split_end[2]) + 1
        end_datetime_filter = datetime(end_year, end_month, end_day)

    if user_all_cnt == "":
        myclass_info = select_myclass_list_date(user_id, start_datetime_filter, end_datetime_filter)
        total = myclass_info.count()
    else:
        total = user_all_cnt

    user_info = select_register(user_id)
    start_cnt = 0
    end_cnt = 0
    last_page = int(total) / page_cnt
    reamin = int(total) % page_cnt

    if reamin > 0:
        last_page = int(last_page) + 1

    for count in range(0, paging_num):
        if paging_num > 1:
            start_cnt = end_cnt
        end_cnt = start_cnt + page_cnt

    myclass_info_paging = select_myclass_list_date_paging(user_id, start_datetime_filter, end_datetime_filter, start_cnt, end_cnt)

    context = {
        "myclass_info": myclass_info_paging,
        "user_info": user_info[0],
        "total_count": total,
        "start_date": start_date,
        "end_date": end_date,
        "search": user_id,
        "last_page": int(last_page),
        "paging_num":paging_num,
    }

    return render(request, 'runAdmin/user_list.html', context)

def user_refund(request):
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    user_id = request.POST['searchBox']
    total = request.POST['user_all_cnt']  # payInfo total count
    paging_num = 1 # 옮기고자 하는 paging 번호
    page_cnt = display_count  # display count 노출되는 리스트 갯수

    pay_num = request.POST['pay_num']

    refund(pay_num, user_id)

    start_datetime_filter = ""
    end_datetime_filter = ""

    if start_date is not "":
        split_start = start_date.split('-')
        start_year = int(split_start[0])
        start_month = int(split_start[1])
        start_day = int(split_start[2])
        start_datetime_filter = datetime(start_year, start_month, start_day)

    if end_date is not "":
        split_end = end_date.split('-')
        end_year = int(split_end[0])
        end_month = int(split_end[1])
        end_day = int(split_end[2]) + 1
        end_datetime_filter = datetime(end_year, end_month, end_day)


    user_info = select_register(user_id)
    start_cnt = 0
    end_cnt = 0
    last_page = int(total) / page_cnt
    reamin = int(total) % page_cnt

    if reamin > 0:
        last_page = int(last_page) + 1

    for count in range(0, paging_num):
        if paging_num > 1:
            start_cnt = end_cnt
        end_cnt = start_cnt + page_cnt

    myclass_info_paging = select_myclass_list_date_paging(user_id, start_datetime_filter, end_datetime_filter, start_cnt, end_cnt)

    context = {
        "myclass_info": myclass_info_paging,
        "user_info": user_info[0],
        "total_count": total,
        "start_date": start_date,
        "end_date": end_date,
        "search": user_id,
        "last_page": int(last_page),
        "paging_num":paging_num,
    }

    return render(request, 'runAdmin/user_list.html', context)
