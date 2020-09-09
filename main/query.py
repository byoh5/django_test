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
    prd_info = PrdTB.objects.filter(keyword=keyword, dbstat='A')
    return prd_info

def select_pay(pay_idx):
    pay_info = PayTB.objects.filter(pay_idx=pay_idx)
    return pay_info

def select_pay_user(user_id):
    pay_info = PayTB.objects.filter(user_id=user_id)
    return pay_info

def select_myclass_list(user_id):
    myclass_list_info = MyClassListTB.objects.filter(user_id=user_id, dbstat='A')
    return myclass_list_info

def select_class_list():
    prd_info = PrdTB.objects.filter(dbstat='A')
    return prd_info

def select_class_detail(prd_code):
    item_info = ItemTB.objects.filter(prd_code=prd_code)
    return item_info

def select_downdata(prdCode):
    downdata_info = ItemDowndataTB.objects.filter(prd_code=prdCode)
    return downdata_info

def select_lounge():
    lounge_info = loungeListTB.objects.filter(dbstat='A')
    return lounge_info

def update_user_addr(user_id, name, add01,add02,add03):
    user_info = select_register(user_id)

    if user_info.count() is not 0:
        new_user = user_info[0]
        new_user.regi_receiver1_name = name
        new_user.regi_receiver1_add01 = add01
        new_user.regi_receiver1_add02 = add02
        new_user.regi_receiver1_add03 = add03
        new_user.save()

        return new_user

def update_user_addr2(user_id, name, add01,add02,add03):
    user_info = select_register(user_id)

    if user_info.count() is not 0:
        new_user = user_info[0]
        new_user.regi_receiver2_name = name
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

