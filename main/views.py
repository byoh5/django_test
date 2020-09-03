from django.http import HttpResponse
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


delete_on = 1
delete_off = 0

def index(request):
    return render(request, 'main/index_runcoding.html')

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