from main.query import *
from main.models import *
import string
import random

def stat_menu_step(request, main, sub, search):
    session = request.session.get('client_id', '')
    user_id = request.session.get('user_id')

    if user_id == '' and session == '':
        number_pool = string.digits
        _LENGTH = 8
        session = str(timezone.now().month) + str(timezone.now().day) + str(timezone.now().hour) + str(
            timezone.now().minute) + "-"
        for i in range(_LENGTH):
            session += random.choice(number_pool)
        request.session['client_id'] = session
        user = session
    else:
        if user_id == '':
            user = session
        else:
            user = user_id

    stat_menu_info = stat_menu(user=user, main_menu=main, sub_menu=sub, info_search_etc=search)
    stat_menu_info.save()