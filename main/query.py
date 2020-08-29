from main.models import *
from django.utils import timezone

def select_order(user_id):
    order_info = OrderTB.objects.filter(user_id=user_id, dbstat='A')
    return order_info

def select_order_idx(idx, user_id):
    order_info = OrderTB.objects.filter(order_idx=idx, user_id=user_id, dbstat='A')
    return order_info

def select_order_prdCode(user_id, prd_code):
    order_info = OrderTB.objects.filter(user_id=user_id, prd_code=prd_code, dbstat='A')
    return order_info

def select_login(user_id):
    login_info = LoginTB.objects.filter(user_id=user_id, dbstat='A')
    return login_info

def select_register(regi_id):
    regi_info = RegisterTB.objects.filter(regi_id=regi_id, dbstat='A')
    return regi_info

def select_prd(prd_code):
    prd_info = PrdTB.objects.filter(prd_code=prd_code, dbstat='A')
    return prd_info

def select_pay(pay_idx):
    pay_info = PayTB.objects.filter(pay_idx=pay_idx)
    return pay_info

def update_order_prdCode(order_prd_info):
    new_orderPrd = order_prd_info[0]
    new_orderPrd.count = new_orderPrd.count + 1
    new_orderPrd.save()

def update_order_idx(idx, user_id, count):
    order_info = select_order_idx(idx, user_id)
    prd_title = ""

    print(order_info.count())
    if order_info.count() is not 0:
        prd_title = order_info[0].prd.title
        new_order = order_info[0]
        new_order.count = count
        new_order.save()

    return prd_title

def delete_order_idx(idx, user_id):
    order_info = select_order_idx(idx, user_id)

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

