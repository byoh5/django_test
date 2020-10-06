from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from main.query import *
from main.models import *

def deposit_list(request):
    return render(request, 'runAdmin/deposit_list.html')

def deposit_search(request):
    userid = request.session.get('user_id')
    user_info = select_register(userid)

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
            end_day = int(split_end[2])
            end_datetime_filter = datetime(end_year, end_month, end_day)

            pay_info = select_pay_date_deposit(start_datetime_filter, end_datetime_filter, searchBox)
            myclass_list_info = select_myclass_date_deposit(start_datetime_filter, end_datetime_filter)

            context = {
                "pay_info": pay_info,
                "total_count":pay_info.count(),
                "myclass_list":myclass_list_info,
                "start_date": start_date,
                "end_date": end_date,
            }
            return render(request, 'runAdmin/deposit_list.html', context)
        else:
            disableSession(userid, request)
    else:
        return render(request, 'login/login.html')

def deposit_change(request):
    pay_num = request.POST['pay_num']
    user_id = request.POST['user_id']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    searchBox = request.POST['searchBox']

    myclass_list_info = select_myclass_list_payNum(user_id, pay_num)
    for myclass_list in myclass_list_info:
        new_myclass_list = myclass_list
        new_myclass_list.dbstat = 'A'
        new_myclass_list.save()

    split_start = start_date.split('-')
    start_year = int(split_start[0])
    start_month = int(split_start[1])
    start_day = int(split_start[2])
    start_datetime_filter = datetime(start_year, start_month, start_day)

    split_end = end_date.split('-')
    end_year = int(split_end[0])
    end_month = int(split_end[1])
    end_day = int(split_end[2])
    end_datetime_filter = datetime(end_year, end_month, end_day)

    pay_info = select_pay_date_deposit(start_datetime_filter, end_datetime_filter, searchBox)
    myclass_list_info = select_myclass_date_deposit(start_datetime_filter, end_datetime_filter)

    context = {
        "pay_info": pay_info,
        "total_count": pay_info.count(),
        "myclass_list": myclass_list_info,
        "start_date": start_date,
        "end_date": end_date,
    }
    return render(request, 'runAdmin/deposit_list.html', context)

def pay_list(request):
    return render(request, 'runAdmin/pay_list.html')

def pay_search(request):
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
    end_day = int(split_end[2])
    end_datetime_filter = datetime(end_year, end_month, end_day)

    pay_info = select_pay_date(start_datetime_filter, end_datetime_filter, searchBox)
    order_info = select_order_date(start_datetime_filter, end_datetime_filter, searchBox)
    context = {
        "pay_info": pay_info,
        "total_count": pay_info.count(),
        "start_date": start_date,
        "end_date": end_date,
        "order_info": order_info,
    }

    return render(request, 'runAdmin/pay_list.html', context)




