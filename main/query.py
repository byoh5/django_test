from main.models import *
from django.utils import timezone
from django.db.models import Q

def select_order(user_id):
    order_info = OrderTB.objects.filter(user_id=user_id, dbstat='A')
    return order_info

def select_order_idx(idx, user_id):
    order_info = OrderTB.objects.filter(order_idx=idx, user_id=user_id, dbstat='A')
    return order_info

def select_order_prdCode(user_id, prd_code):
    order_info = OrderTB.objects.filter(user_id=user_id, prd__prd_code=prd_code, dbstat='A')
    return order_info

def select_login(user_id):
    login_info = LoginTB.objects.filter(user_id=user_id, dbstat='A')
    return login_info

def select_register(regi_email):
    regi_info = RegisterTB.objects.filter(regi_email=regi_email, dbstat='A')
    return regi_info

def select_register_all(regi_email):
    regi_info = RegisterTB.objects.filter(regi_email=regi_email)
    return regi_info

def select_prd(prd_code):
    prd_info = PrdTB.objects.filter(prd_code=prd_code, dbstat='A')
    return prd_info

def select_prd_keyword(keyword):
    prd_info = PrdTB.objects.filter(Q(keyword=keyword, dbstat='A') | Q(title__icontains=keyword, dbstat='A') | Q(title2__icontains=keyword, dbstat='A') | Q(title3__icontains=keyword, dbstat='A'))
    return prd_info

def select_pay(pay_idx):
    pay_info = PayTB.objects.filter(pay_idx=pay_idx)
    return pay_info

def select_pay_user(user_id):
    pay_info = PayTB.objects.filter(pay_user__regi_email=user_id).order_by('-pay_idx')
    return pay_info

def select_myclass_list(user_id):
    myclass_list_info = MyClassListTB.objects.filter(user_id=user_id, dbstat='A')
    return myclass_list_info

def select_class_list():
    prd_info = PrdTB.objects.filter(dbstat='A')
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

def update_order_prdCode(order_prd_info):
    new_orderPrd = order_prd_info[0]
    new_orderPrd.count = new_orderPrd.count + 1
    new_orderPrd.save()

def update_order_idx(idx, user_id, count, addr_num):
    order_info = select_order_idx(idx, user_id)
    prd_title = ""

    if order_info.count() is not 0:
        prd_title = order_info[0].prd.title
        new_order = order_info[0]
        new_order.count = count
        new_order.delevery_addr_num = addr_num
        new_order.save()

    return prd_title

def delete_order_idx(order_info):
    if order_info.count() is not 0:
        new_order = order_info[0]
        new_order.dbstat = 'D-'
        new_order.save()

def delete_login(user_id):
    login_info = select_login(user_id)
    if login_info.count() is not 0:
        new_login = login_info[0]
        new_login.dbstat = 'D-'

        new_login.logout_time = timezone.now()
        new_login.save()

