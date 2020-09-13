from django.contrib import admin
from main.models import *
from .models import RegisterTB
from .models import LoginTB
from .models import PrdTB
from .models import ItemTB
from .models import OrderTB
from .models import PayTB
from .models import MyClassListTB
from .models import ItemDowndataTB
from .models import loungeListTB
from .models import comunityTB
from .models import categoryTB

# Register your models here.

class RegisterAdmin(admin.ModelAdmin):
    list_display = ['regi_idx', 'regi_email', 'regi_name', 'regi_phone', 'stime', 'dbstat'] # 커스터마이징 코드
    list_display_links = ['regi_email', 'regi_name']

    list_filter = ['stime', 'dbstat']
    search_fields = ['regi_email', 'regi_name']

admin.site.register(RegisterTB, RegisterAdmin)

class LoginAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'login_time', 'dbstat'] # 커스터마이징 코드
    list_display_links = ['user_id']
    list_filter = ['login_time', 'dbstat']
    search_fields = ['user_id']

admin.site.register(LoginTB,LoginAdmin)

class PrdAdmin(admin.ModelAdmin):
    list_display = ['prd_code', 'title', 'period', 'price', 'keyword', 'dbstat'] # 커스터마이징 코드
    list_display_links = ['prd_code']
    list_filter = ['prd_code', 'dbstat']

    search_fields = ['prd_code', 'title', 'keyword']

admin.site.register(PrdTB, PrdAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'title', 'order'] # 커스터마이징 코드

    def get_name(self, obj):
        return obj.prd.prd_code

    get_name.short_description = 'prd code'  # Renames column head

    list_display_links = ['title']
    search_fields = ['title']

admin.site.register(ItemTB, ItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'get_name', 'count', 'order_time', 'dbstat'] # 커스터마이징 코드

    def get_name(self, obj):
        return obj.prd.prd_code

    get_name.short_description = 'prd code'  # Renames column head

    list_filter = ['order_time', 'dbstat']
    list_display_links = ['user_id']
    search_fields = ['user_id']

admin.site.register(OrderTB, OrderAdmin)

class PayAdmin(admin.ModelAdmin):
    list_display = ['pay_num', 'get_name', 'prd_info', 'prd_total_price', 'pay_result', 'pay_time'] # 커스터마이징 코드

    list_filter = ['pay_time', 'pay_result']

    def get_name(self, obj):
        return obj.pay_user.regi_email

    get_name.short_description = 'pay_user'  # Renames column head

    list_display_links = ['pay_num']
    search_fields = ['pay_user']

admin.site.register(PayTB, PayAdmin)

class MyClassListAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'get_name', 'start_time', 'expire_time', 'dbstat'] # 커스터마이징 코드

    list_filter = ['start_time', 'expire_time','dbstat']
    def get_name(self, obj):
        return obj.prd.prd_code

    get_name.short_description = 'prd code'  # Renames column head

    list_display_links = ['user_id']
    search_fields = ['user_id']

admin.site.register(MyClassListTB, MyClassListAdmin)


class ItemDowndataAdmin(admin.ModelAdmin):
    list_display = ['downdata_idx', 'downdata_name', 'prd_code', 'dbstat']  # 커스터마이징 코드

    list_filter = ['dbstat']

    list_display_links = ['downdata_idx', 'downdata_name']
    search_fields = ['downdata_name', 'prd_code']

admin.site.register(ItemDowndataTB, ItemDowndataAdmin)

class loungeListAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'data_name', 'video_id', 'dbstat']  # 커스터마이징 코드

    list_filter = ['dbstat']

    list_display_links = ['title', 'video_id']
    search_fields = ['video_id', 'title', 'user']

admin.site.register(loungeListTB, loungeListAdmin)

class comunityAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'dbstat']  # 커스터마이징 코드

    list_filter = ['dbstat']
    list_display_links = ['category', 'title']
    search_fields = ['category', 'title']

admin.site.register(comunityTB, comunityAdmin)

class categoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'dbstat']  # 커스터마이징 코드

    list_filter = ['dbstat']
    list_display_links = ['name']
    search_fields = ['name']

admin.site.register(categoryTB, categoryAdmin)
