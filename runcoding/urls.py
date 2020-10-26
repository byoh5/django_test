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
from main.codeView.lecture import *
from main.codeView.comunity import *
from main.codeView.login import *
from main.codeView.lounge import *
from main.codeView.myclass import *
from main.codeView.mypage import *
from main.codeView.order import *
from main.codeView.payment import *
from main.codeView.regi import *
from main.codeView.search import *
from main.codeView.confirm_user import *
from main.codeView.runAdmin import *
from main.codeView.watch import *

urlpatterns = [
    path('regi/', register_page),
    path('run_login/', login_page),
    path('register/', UserRegister),
    path('login_form/', login),
    path('run_logout/', logout),
    path('check_id/', check_id_popup),

    path('class/', class_page),
    path('class_detail/', class_detail_page),
    path('detail_prd/', class_detail_page_prd),

    path('myclass/', myclass_page),
    path('myclass_list/', myclass_list_page),
    path('video_play/',video_play_page),

    path('comunity/', comunity_page),
    path('get_category/', comunity_page_category),

    path('lounge/', lounge_page),
    path('lounge_view/', loungeView_page),
    path('lounge_page_paging/', lounge_page_paging),

    path('order/', order_page),
    path('order_del/', order_delete),
    path('run_pay/', payment),
    path('run_order/', order),
    path('pay_result/', pay_result),

    path('myprofile/', mypage_profile),
    path('myorder/', mypage_order),
    path('myorder_detail/', mypage_order_detail),
    path('myorder_refund/', mypage_order_refund),

    path('my_modify_addr/', mypage_profile_modify_addr),
    path('my_modify_addr2/', mypage_profile_modify_addr2),
    path('my_modify_pw/', mypage_profile_modify_pw),

    path('coupon/', mypage_coupon_list),
    path('add_coupon/', mypage_add_coupon),

    path('contact_email/', contact_email),
    path('find_pass/', find_pass_viaEmail),
    path('info_email/', info_email),

    path('search/', search_prd),

    path('confirm/', getConfirm),

    path('deposit_list/', deposit_list),
    path('deposit_search/', deposit_search),
    path('deposit_change/', deposit_change),
    path('pay_list/', pay_list),
    path('pay_search/', pay_search),
    path('pay_change/', pay_change),
    path('user_list/',user_list),
    path('user_search/', user_search),
    path('user_refund/', user_refund),

    path('watchCam/', watch_esp_cam),

    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]
