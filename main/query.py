from main.models import *
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render

def select_order(user_id):
    order_info = OrderTB.objects.filter(user_id=user_id, dbstat='A')
    return order_info

def select_order_idx(idx, user_id):
    order_info = OrderTB.objects.filter(order_idx=idx, user_id=user_id, dbstat='A')
    return order_info

def select_order_payNum(pay_num, user_id):
    order_info = OrderTB.objects.filter(pay_num=pay_num, user_id=user_id)
    return order_info

def select_order_info(idx, user_id):
    order_info = OrderTB.objects.filter(order_idx=idx, user_id=user_id)
    return order_info

def select_order_prdCode(user_id, prd_code):
    order_info = OrderTB.objects.filter(user_id=user_id, prd__prd_code=prd_code, dbstat='A')
    return order_info
#
def select_order_date(start_datetime_filter, end_datetime_filter, search):
    sort_order = '-order_idx'

    query_search = Q()

    if search is not "":
        query_search.add(Q(user_id__icontains=search) | Q(pay_num__icontains=search), query_search.AND)

    order_pay_info = OrderTB.objects.filter(query_search, pay_num__icontains='-',
                                            modified__range=(start_datetime_filter.date(), end_datetime_filter.date())).order_by(sort_order)
    return order_pay_info

def select_register(regi_email):
    regi_info = RegisterTB.objects.filter(regi_email=regi_email, dbstat='A')
    return regi_info

def select_register_all(regi_email):
    regi_info = RegisterTB.objects.filter(regi_email=regi_email)
    return regi_info

def select_register_idx(idx):
    regi_info = RegisterTB.objects.filter(regi_idx=idx, dbstat='A')
    return regi_info

def select_login(user_id):
    login_info = LoginTB.objects.filter(user_id=user_id, dbstat='A')
    return login_info

def select_prd(prd_code):
    prd_info = PrdTB.objects.filter(prd_code=prd_code, dbstat='A')
    return prd_info

def select_prd_keyword(keyword):
    prd_info = PrdTB.objects.filter(Q(keyword=keyword, dbstat='A') | Q(title__icontains=keyword, dbstat='A') | Q(title2__icontains=keyword, dbstat='A') | Q(title3__icontains=keyword, dbstat='A'))
    return prd_info

def select_userStatue(userStatus_idx):
    userStatus_info = UserStatusTB.objects.filter(userStatus_idx=userStatus_idx)
    return userStatus_info

def select_userStatus_all():
    userStatus_info = UserStatusTB.objects.filter(dbstat='A')
    return userStatus_info

def select_pay(pay_idx):
    pay_info = PayTB.objects.filter(pay_idx=pay_idx)
    return pay_info

def select_pay_user(user_id):
    pay_info = PayTB.objects.filter(pay_user__regi_email=user_id).order_by('-pay_idx')
    return pay_info

def select_pay_user_payNume(user_id, pay_num):
    pay_info = PayTB.objects.filter(pay_user__regi_email=user_id, pay_num=pay_num).order_by('-pay_idx')
    return pay_info

def select_pay_date_deposit(start_datetime_filter, end_datetime_filter, search):
    pay_info = PayTB.objects.filter(pay_time__range=(start_datetime_filter.date(), end_datetime_filter.date()),
                                    payWay__value='deposit', pay_user__regi_email__icontains=search).order_by('-pay_idx')
    return pay_info

def select_pay_date(start_datetime_filter, end_datetime_filter, search, status):
    sort_order = '-pay_idx'

    query_search = Q()

    if int(status) > 0:
        query_search.add(Q(pay_user_status__userStatus_idx=status), query_search.AND)

    if search is not "":
        query_search.add(Q(pay_user__regi_email__icontains=search) | Q(pay_num__icontains=search), query_search.AND)

    pay_info = PayTB.objects.filter(query_search, pay_time__range=(start_datetime_filter.date(), end_datetime_filter.date())).order_by(sort_order)

    return pay_info

def select_pay_date_cnt(start_datetime_filter, end_datetime_filter, search, status, start_cnt, end_cnt ):
    sort_order = '-pay_idx'

    query_search = Q()

    if int(status) > 0:
        query_search.add(Q(pay_user_status__userStatus_idx=status), query_search.AND)

    if search is not "":
        query_search.add(Q(pay_user__regi_email__icontains=search) | Q(pay_num__icontains=search), query_search.AND)

    pay_info = PayTB.objects.filter(query_search, pay_time__range=(start_datetime_filter.date(), end_datetime_filter.date())).order_by(sort_order)[start_cnt:end_cnt]

    return pay_info

def select_myclass_date_deposit(start_datetime_filter, end_datetime_filter):
    myclass_list_info = MyClassListTB.objects.filter(start_time__range=(start_datetime_filter.date(), end_datetime_filter.date()))
    return myclass_list_info

def select_myclass_list_idx(idx):
    myclass_list_info = MyClassListTB.objects.filter(myclassList_idx=idx, dbstat='D-deposit')
    return myclass_list_info

def select_myclass_list(user_id):
    myclass_list_info = MyClassListTB.objects.filter(user_id=user_id, dbstat='A')
    return myclass_list_info

def select_myclass_list_payNum(user_id, pay_num):
    myclass_list_info = MyClassListTB.objects.filter(user_id=user_id, pay_num=pay_num, dbstat='D-deposit')
    return myclass_list_info

def select_class_list():
    prd_info = PrdTB.objects.filter(dbstat='A').order_by('-prd_idx')
    return prd_info

def select_class_detail(prd_code):
    item_info = ItemTB.objects.filter(prd__prd_code=prd_code).order_by('order')
    return item_info

def select_downdata(prdCode):
    downdata_info = ItemDowndataTB.objects.filter(prd_code=prdCode)
    return downdata_info

def select_lounge():
    lounge_info = loungeListTB.objects.filter(dbstat='A').order_by('-loungeList_idx')
    return lounge_info

def select_lounge_cnt(start_cnt, end_cnt):
    lounge_info = loungeListTB.objects.filter(dbstat='A').order_by('-loungeList_idx')[start_cnt:end_cnt]
    return lounge_info

def select_lounge_search(sort, category, keyword):
    sort_order = 'loungeList_idx'
    if sort == 'new':
        sort_order = '-loungeList_idx'

    query_search = Q()

    if int(category) > 0:
        query_search.add(Q(loungeList_idx=category), query_search.AND)

    if keyword is not "":
        query_search.add(Q(title__icontains=keyword) | Q(user__icontains=keyword), query_search.AND)

    lounge_info = loungeListTB.objects.filter(query_search, dbstat='A').order_by(sort_order)

    return lounge_info


def select_lounge_search_cnt(sort, category, keyword, start_cnt, end_cnt):
    sort_order = 'loungeList_idx'
    if sort == 'new':
        sort_order = '-loungeList_idx'

    query_search = Q()

    if int(category) > 0:
        query_search.add(Q(loungeList_idx=category), query_search.AND)

    if keyword is not "":
        query_search.add(Q(title__icontains=keyword) | Q(user__icontains=keyword), query_search.AND)

    lounge_info = loungeListTB.objects.filter(query_search, dbstat='A').order_by(sort_order)[start_cnt:end_cnt]

    return lounge_info

def select_lounge_categoy():
    category_info = loungeListTB.objects.filter(dbstat='A').only("data_name", "loungeList_idx")
    return category_info

def select_comunity():
    comunity_info = comunityTB.objects.filter(dbstat='A')
    return comunity_info

def select_category():
    category_info = categoryTB.objects.filter(dbstat='A')
    return category_info

def select_comunity_category(idx):
    comunity_info = comunityTB.objects.filter(category__category_idx=idx, dbstat='A')
    return comunity_info

def select_runcoding():
    runcoding_info = runcodingTB.objects.filter(runcoding_idx=1)
    return runcoding_info

def select_myCoupon(user_id):
    myCoupon_info = myCouponTB.objects.filter(user__regi_email=user_id, dbstat='A')
    return myCoupon_info

def select_myCoupon_notUsed(user_id):
    myCoupon_info = myCouponTB.objects.filter(user__regi_email=user_id, used=False, dbstat='A')
    return myCoupon_info

def select_myCoupon_couponNum(user_id, coupon_num):
    myCoupon_info = myCouponTB.objects.filter(user__regi_email=user_id, coupon__coupon_num=coupon_num, dbstat='A')
    return myCoupon_info

def select_coupon(coupon_num):
    coupon_info = couponTB.objects.filter(coupon_num=coupon_num, dbstat='A')
    return coupon_info

def select_coupon_all(coupon_num):
    coupon_info = couponTB.objects.filter(coupon_num=coupon_num)
    return coupon_info

def select_payway():
    payway_info = PayWayTB.objects.filter(dbstat='A')
    return payway_info

def select_payway_value(value):
    payway_info = PayWayTB.objects.filter(dbstat='A', value=value)
    return payway_info

def update_user_addr(user_id, add01,add02,add03):
    user_info = select_register(user_id)

    if user_info.count() is not 0:
        new_user = user_info[0]
        new_user.regi_receiver1_add01 = add01
        new_user.regi_receiver1_add02 = add02
        new_user.regi_receiver1_add03 = add03
        new_user.save()

        return new_user

def update_user_addr2(user_id, name, phone, add01,add02,add03):
    user_info = select_register(user_id)

    if user_info.count() is not 0:
        new_user = user_info[0]
        new_user.regi_receiver2_name = name
        new_user.regi_receiver2_phone = phone
        new_user.regi_receiver2_add01 = add01
        new_user.regi_receiver2_add02 = add02
        new_user.regi_receiver2_add03 = add03
        new_user.save()

        return new_user

def update_order_prdCode(order_prd_info, count, option1, option2, option3):
    new_orderPrd = order_prd_info[0]
    new_orderPrd.count = new_orderPrd.count + int(count)
    new_orderPrd.option1_selectNum = option1
    new_orderPrd.option2_selectNum = option2
    new_orderPrd.option3_selectNum = option3
    new_orderPrd.save()

def update_order_idx(count, order_info, addr_num, option1, option2, option3):
    new_order = order_info[0]
    new_order.count = count
    new_order.delevery_addr_num = addr_num
    new_order.option1_selectNum = option1
    new_order.option2_selectNum = option2
    new_order.option3_selectNum = option3
    new_order.save()

def update_myCoupon(user_id, coupon_num):
    myCoupon_info = select_myCoupon_couponNum(user_id, coupon_num)

    if myCoupon_info.count() is not 0:
        update_myCoupon = myCoupon_info[0]
        update_myCoupon.used = True
        update_myCoupon.save()

def delete_order_idx(order_info, pay_num):
    if order_info.count() is not 0:
        new_order = order_info[0]
        new_order.dbstat = 'D-'
        new_order.pay_num = pay_num
        new_order.save()

def delete_login(user_id):
    login_info = select_login(user_id)
    if login_info.count() is not 0:
        new_login = login_info[0]
        new_login.dbstat = 'D-'

        new_login.logout_time = timezone.now()
        new_login.save()

def changePhone_format(number):
   phone = ""
   if len(number) < 10 : #010-123-123
        phone += number[0:3]
        phone += "-"
        phone += number[3:6]
        phone += "-"
        phone += number[6:9]
   elif  len(number) < 11 : #010-123-1234
        phone += number[0:3]
        phone += "-"
        phone += number[3:6]
        phone += "-"
        phone += number[6:10]
   else:
        phone += number[0:3]
        phone += "-"
        phone += number[3:7]
        phone += "-"
        phone += number[7:11]

   return phone

def checkSession(session, user_id):
    loginUser_info = select_login(user_id)

    if loginUser_info.count() is not 0 and session is not None:
        if loginUser_info[0].session_id == session:
            return 1
        else:
            return 0
    else:
        return 0

message_no_login = 210
def disableSession(userid, request):
    delete_login(userid)
    request.session['client_id'] = ''
    request.session['user_id'] = ''
    context = {
        "msg": message_no_login,
    }
    return render(request, 'login/login.html', context)