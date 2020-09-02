from django.shortcuts import render, redirect
from main.models import *
from main.query import *
import bcrypt
from django.utils import timezone
from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.middleware.csrf import *
# from main.naver import *
from django.contrib.auth import get_user_model
# from django.http import HttpResponse, HttpResponseRedirect

# RegisterTB 테이블 import 확인하기

# login
message_ok = 200
message_diff_pass = 202
message_no_regi = 204
message_exist_id = 208

delete_on = 1
delete_off = 0

pay_ok = 0
pay_fail = 1


def index(request):
    return render(request, 'main/index_runcoding.html')


def index_page(request):
    return render(request, 'main/index.html')


def register_page(request):
    return render(request, 'login/register.html')


def login_page(request):
    return render(request, 'login/login.html')


def naverLogin_page(request):
    return render(request, 'login/naverlogin.html')


def class_page(request):
    class_list_info = select_class_list()
    context = {
        "class_list_detail": class_list_info,
    }

    return render(request, 'class/class_list.html', context)

def class_detail_page(request):
    prd_code = request.POST['detail_prd_code']
    items_info = select_class_detail(prd_code)

    context = {
        "class_items_detail": items_info,
        "prd_detail": items_info[0].prd,
    }

    return render(request, 'class/class_detail.html', context)


def myclass_list_page(request):
    user_id = request.session.get('user_id')
    myclass_list_info = select_myclass_list(user_id)

    context = {
        "myclass_list_detail": myclass_list_info,
    }

    return render(request, 'myclass/myclass_list.html', context)


def myclass_page(request):
    prdCode = request.POST['prdCode']

    item_info = select_class_detail(prdCode)
    downdata_info = select_downdata(prdCode)

    if item_info.count() is not 0:
        context = {
            "myclass_detail": item_info,
            "title": item_info[0].prd.title2,
            "sub_title": item_info[0].prd.title3,
            "downData": downdata_info,
        }
        return render(request, 'myclass/myclass.html', context)


def comunity_page(request):
    return render(request, 'comunity/coding_comunity.html')


def lounge_page(request):
    return render(request, 'lounge/coding_lounge.html')


def loungeView_page(request):
    return render(request, 'lounge/coding_lounge_view.html')

def order_page(request):
    session = request.session.get('client_id')
    userid = request.session.get('user_id')  # 이 값으로 디비에서 정보찾고..
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

# id로 검색해서 없으면 진행...있으면 에러리턴.
def UserRegister(request):
    regi_id = request.POST['regi_id']
    regi_info = select_register(regi_id)  # 회원가입 요청한 ID 가입자 아님을 더블체크

    if regi_info.count() is 0:
        password = request.POST['regi_pass']
        password_encrypt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        q = RegisterTB(regi_id=regi_id, regi_name=request.POST['regi_name'],
                       regi_phone=request.POST['regi_phone'], regi_email=request.POST['regi_email'],
                       regi_add01=request.POST['regi_add01'], regi_add02=request.POST['regi_add02'],
                       regi_add03=request.POST['regi_add03'], regi_pass=password_encrypt.decode('utf-8'))
        q.save()
        return render(request, 'login/login.html')  # 로그인페이지호출
    else:
        context = {
            "popup_message": message_exist_id,
            "regiId": regi_id,
        }
        return render(request, 'login/register.html', context)  # register page에서 메시지 출력 이미 가입자입니다.


def login(request):
    if request.method == "POST":
        login_id = request.POST['login_id']
        regi_info = select_register(login_id)
        if regi_info.count() is not 0:
            password_encrypt = regi_info[0].regi_pass
            regi_id = regi_info[0].regi_id
            login_password = request.POST['login_pass']
            check_pass = bcrypt.checkpw(login_password.encode('utf-8'), password_encrypt.encode('utf-8'))
            if check_pass:
                session_auth = bcrypt.hashpw(regi_id.encode('utf-8'), bcrypt.gensalt())
                session = session_auth.decode('utf-8')
                delete_login(login_id)
                q = LoginTB(user_id=login_id, session_id=session)
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
    print(regi_id)
    if regi_info.count() is not 0:
        context = {
            "popup_message": message_exist_id,  # 전역 변수로 변경 필요
            "regiId":regi_id,
        }
    else:
        context = {
            "popup_message": message_ok,
            "regiId": regi_id,
        }
    return render(request, 'login/register.html', context)

def order(request):
    user_id = request.session.get('user_id')
    prd_code = request.POST['prd_code']
    login_info = select_login(user_id)
    messages = 0
    if login_info.count() is not 0:
        order_prd_info = select_order_prdCode(user_id, prd_code)
        if order_prd_info.count() is not 0:
            update_order_prdCode(order_prd_info)
            messages = 1  # 성공
        else:
            prd_info = select_prd(prd_code)
            order = OrderTB(user_id=user_id, prd_code=prd_code, prd=prd_info[0])
            order.save()
            messages = 1  # 성공

    items_info = select_class_detail(prd_code)
    context = {
        "message": messages,
        "class_items_detail": items_info,
        "prd_detail": items_info[0].prd,
    }
    return render(request, 'class/class_detail.html', context)

def payment(request):
    user_id = request.session.get('user_id')
    order_len = request.POST['len']
    prd_price = int(request.POST['total_prd_price'])
    option_price = int(request.POST['total_option_price'])
    prd_total_price = int(request.POST['total_option_prd_price'])

    order_list = ""
    prd_title = ""
    prd_total_count = 0

    for cnt in range(int(order_len)):
        idx = request.POST['orderIdxs_' + str(cnt)]
        prd_count = request.POST['prodQuantity_' + str(cnt)]
        prd_total_count += int(prd_count)
        prd_title = update_order_idx(idx, user_id, prd_count) #count 변경 되었을 수 있으니 정보 update 및 상품 title get
        order_list += idx + ","

    if prd_total_count > 1:
        prd_title += "_외 " + str(prd_total_count) + "개"

    regi_info = select_register(user_id)

    pay_info = PayTB(user_id=user_id, pay_user=regi_info[0], order_id=order_list, prd_info=prd_title,
          prd_price=prd_price, delivery_price=option_price, prd_total_price=prd_total_price)
    pay_info.save()

    context = {
        "payment": pay_info,
    }

    return render(request, 'payment/pay_info.html', context)

def pay_result(request):
    pay_idx = int(request.POST['pay'])
    user_id = request.session.get('user_id')

    pay_result = int(request.POST['pay_result'])
    pay_msg = request.POST['pay_msg']

    pay_info = select_pay(pay_idx)

    if pay_info.count() is not 0:
        update_pay = pay_info[0]
        update_pay.pay_result_info = pay_msg
        update_pay.pay_result = pay_result

        if pay_result == pay_ok:
            split_order = update_pay.order_id.split(',')
            
            # product -> myclass에 넣고, 장바구니 정리하기
            for data in split_order:
                if len(data) > 0:
                    order_info = select_order_idx(data, user_id)

                    if order_info.count() is not 0:
                        # insert myclass_list
                        period = order_info[0].prd.period * 60
                        expireTime = timezone.now() + timezone.timedelta(days=period)
                        myclass_list_info = MyClassListTB(user_id=user_id, prd=order_info[0].prd, expire_time=expireTime)
                        myclass_list_info.save()

                    delete_order_idx(order_info)  # order dbstat 변경

        update_pay.save()

    if pay_result == pay_ok:
        myclass_list_info = select_myclass_list(user_id)

        context = {
            "myclass_list_detail": myclass_list_info,
        }

        return render(request, 'myclass/myclass_list.html', context)
    else:
        order_info = select_order(user_id)
        user_info = select_register(user_id)
        context = {
            "order_detail": order_info,
            "user_detail": user_info,
        }

        return render(request, 'payment/order.html', context)


# 스크립트로
# myclass expire되면 dbstat 바꾸는거 진행


# class SocialLoginCallbackView(NaverLoginMixin, View):
#
#     success_url = settings.LOGIN_REDIRECT_URL
#     failure_url = settings.LOGIN_URL
#     required_profiles = ['email', 'name']
#     model = get_user_model()
#
#     def get(self, request, *args, **kwargs):
#
#         provider = kwargs.get('provider')
#         provider='naver'
#
#         if provider == 'naver': # 프로바이더가 naver 일 경우
#             csrf_token = request.GET.get('state')
#             code = request.GET.get('code')
#             print(csrf_token)
#             print(request.COOKIES.get('csrftoken'))
#             print(code)
#             # if not _compare_salted_tokens(csrf_token, request.COOKIES.get('csrftoken')): # state(csrf_token)이 잘못된 경우
#             #     messages.error(request, '잘못된 경로로 로그인하셨습니다.', extra_tags='danger')
#             #     return HttpResponseRedirect(self.failure_url)
#         #     is_success, error = self.login_with_naver(csrf_token, code)
#         #     if not is_success: # 로그인 실패할 경우
#         #         messages.error(request, error, extra_tags='danger')
#         #     return HttpResponseRedirect(self.success_url if is_success else self.failure_url)
#         #
#         # return HttpResponseRedirect(self.failure_url)
#
#     def set_session(self, **kwargs):
#         for key, value in kwargs.items():
#             self.request.session[key] = value