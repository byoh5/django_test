"""runcoding URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main.views import *

urlpatterns = [
    path('regi/', register_page),
    path('run_login/', login_page),
    path('register/', UserRegister),
    path('login_form/', login),
    path('run_logout/', logout),
    path('popup/', popup),
    # path('social_accounts/',SocialLoginCallbackView.as_view()),

    path('class/', class_page),
    path('class_detail/', class_detail_page),

    path('myclass/', myclass_page),
    path('myclass_list/', myclass_list_page),

    path('comunity/', comunity_page),
    path('lounge/', lounge_page),
    path('lounge_view/', loungeView_page),

    path('order/', order_page),
    path('run_pay/', payment),
    path('run_order/', order),
    path('pay_result/', pay_result),

    path('myprofile/', mypage_profile),
    path('myorder/', mypage_order),
    path('my_modify_addr/', mypage_profile_modify_addr),
    path('my_modify_pw/', mypage_profile_modify_pw),

    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),
    path('', include('main.urls')),
]
