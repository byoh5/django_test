from django.shortcuts import render, redirect
from main.models import *
from main.query import *
import bcrypt

# RegisterTB 테이블 import 확인하기

# login
message_ok = 200
message_diff_pass = 202
message_no_regi = 204
message_exist_id = 208


def index(request):
    return render(request, 'main/index_runcoding.html')


def index_page(request):
    return render(request, 'main/index.html')


def register_page(request):
    request.session['IDresult'] = ""
    return render(request, 'login/register.html')


def login_page(request):
    return render(request, 'login/login.html')


def popup_page(request):
    request.session['IDresult'] = ""
    return render(request, 'popup/popup.html')


def class_page(request):
    return render(request, 'class/class_list.html')


def trashcn_arduino_page(request):
    return render(request, 'class/class_view_arduino.html')


def trashcn_mblock_page(request):
    return render(request, 'class/class_view_mblock.html')


def myclass_list_page(request):
    return render(request, 'myclass/myclass_list.html')


def myclass_page(request):
    return render(request, 'myclass/myclass.html')


def comunity_page(request):
    return render(request, 'comunity/coding_comunity.html')


def lounge_page(request):
    return render(request, 'lounge/coding_lounge.html')


def loungeView_page(request):
    return render(request, 'lounge/coding_lounge_view.html')

def order_page(request):
    session = request.session.get('client_id')
    userid = request.session.get('user_id')  # 이 값으로 디비에서 정보찾고..
    # print(session)

    if session is None:
        return render(request, 'login/login.html')
    else:
        order_info = select_order(userid)
        user_info = select_register(userid)
        context = {
            "order_detail": order_info,
            "user_detail": user_info,
        }

        return render(request, 'payment/order.html', context)  # templete에 없으면 호출이 안됨. ajax


def order(request):
    user_id = request.session.get('user_id')
    session = request.session.get('client_id')

    login_info = select_login(user_id)
    session_id = login_info[0].session_id
    messages = 0

    # 에러남 수정해야됨
    # check_session = bcrypt.checkpw(session.encode('utf-8'), session_id.encode('utf-8'))
    # print(check_session)  # true/false
    #
    # if not check_session:
    #     return render(request, 'login/login.html')
    # else:

    # order table에 저장하고 싶은데...resturn 메세지가 있어야 할듯.

    if login_info.count() is not 0:
        prd_code = request.POST['prd_code']
        order_prd_info = select_order_prdCode(user_id, prd_code)
        if order_prd_info.count() is not 0:
            update_order_prdCode(order_prd_info)
            messages = 1  # 성공
        else:
            prd_info = select_prd(prd_code)
            order = OrderTB(user_id=user_id, prd_code=prd_code, prd=prd_info[0])
            order.save()
            messages = 1  # 성공

    context = {
        "message": messages,
    }
    return render(request, 'class/class_view_arduino.html', context)

    # Create your views here.


# id로 검색해서 없으면 진행...있으면 에러리턴.
def UserRegister(request):
    regi_id = request.POST['regi_id']
    regi_info = select_register(regi_id)  # 회원가입 요청한 ID 가입자 아님을 더블체크

    if regi_info.count() is 0:
        password = request.POST['regi_pass']
        password_encrypt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # print(password_encrypt);

        q = RegisterTB(regi_id=regi_id, regi_name=request.POST['regi_name'],
                       regi_phone=request.POST['regi_phone'], regi_email=request.POST['regi_email'],
                       regi_add01=request.POST['regi_add01'], regi_add02=request.POST['regi_add02'],
                       regi_add03=request.POST['regi_add03'], regi_pass=password_encrypt.decode('utf-8'))

        # from datetime import datetime
        # from django.utils import timezone
        # date_str = "2016-02-20 15:03:55"
        # v = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

        q.save()
        return render(request, 'login/login.html')  # 로그인페이지호출
    else:
        return render(request, 'login/register.html')  # register page에서 메시지 출력 이미 가입자입니다.


def login(request):
    if request.method == "POST":
        loginId = request.POST['login_id']
        regi_info = select_register(loginId)
        if regi_info.count() is not 0:
            password_encrypt = regi_info[0].regi_pass
            regi_id = regi_info[0].regi_id
            login_password = request.POST['login_pass']
            check_pass = bcrypt.checkpw(login_password.encode('utf-8'), password_encrypt.encode('utf-8'))
            if check_pass:
                session_auth = bcrypt.hashpw(regi_id.encode('utf-8'), bcrypt.gensalt())
                session = session_auth.decode('utf-8')
                delete_login(loginId)
                q = LoginTB(user_id=loginId, session_id=session)
                q.save()
                request.session['client_id'] = session
                request.session['user_id'] = regi_id
                request.session['result'] = 'success'
                request.user = regi_id
                request.session.modified = True
                context = {
                    "client_id": session,
                    "user_id": regi_id,
                    "result": message_ok,
                }
                return render(request, 'main/index_runcoding.html', context)
            else:
                request.session['result'] = message_diff_pass
                request.session['client_id'] = ''
                context = {
                    "client_id": '',
                    "user_id": regi_id,
                    "result": message_diff_pass,
                }
                return render(request, 'login/login.html', context)
        else:
            request.session['result'] = message_no_regi
            request.session['client_id'] = ''
            context = {
                "client_id": '',
                "user_id": '',
                "result": message_no_regi,
            }
            return render(request, 'login/login.html', context)  # 가입자가 아닙니다.


def logout(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        delete_login(user_id)

    request.session['client_id'] = ''

    return render(request, 'main/index_runcoding.html')


def popup(request):
    regi_id = request.POST['popup_regiId']
    regi_info = select_register(regi_id)

    if regi_info.count() is not 0:
        # print("Exist.....")
        # request.session['IDresult'] = 'exist'

        context = {
            "popup_message": message_exist_id,  # 전역 변수로 변경 필요
        }

    else:
        # print("DoesNotExist.....")
        context = {
            "popup_message": message_ok,
        }
        # request.session['IDresult'] = 'ok'

    return render(request, 'popup/popup.html', context)



