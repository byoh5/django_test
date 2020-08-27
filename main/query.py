from main.models import *
from datetime import datetime

def select_order(user_id):
    order_info = OrderTB.objects.filter(user_id=user_id)
    return order_info

def select_order_prdCode(user_id, prd_code):
    order_info = OrderTB.objects.filter(user_id=user_id, prd_code=prd_code)
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

def update_order_prdCode(order_prd_info):
        new_orderPrd = order_prd_info[0]
        new_orderPrd.count = new_orderPrd.count + 1
        new_orderPrd.save()

def delete_login(user_id):
    login_info = select_login(user_id)

    if login_info.count() is not 0:
        new_login = login_info[0]
        new_login.dbstat = 'D-'
        new_login.logout_time = datetime.now()
        new_login.save()