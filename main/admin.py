from django.contrib import admin
from main.models import *

# Register your models here.

class RegisterAdmin(admin.ModelAdmin):
    list_display = ['regi_idx', 'regi_email', 'regi_name', 'regi_phone', 'stime', 'dbstat', 'modified'] # 커스터마이징 코드
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

class ItemInfoTBAdmin(admin.ModelAdmin):
    list_display = ['ItemInfo_idx', 'title', 'type', 'downdata_name', 'dbstat'] # 커스터마이징 코드

    list_display_links = ['title']
    search_fields = ['title', 'type']
    ordering = ['-ItemInfo_idx']

admin.site.register(ItemInfoTB, ItemInfoTBAdmin)

class ItemCommonTBAdmin(admin.ModelAdmin):
    list_display = ['prd_name', 'prd_code', 'item_code', 'title', 'order'] # 커스터마이징 코드

    def prd_name(self, obj):
        return obj.prd.title

    def prd_code(self, obj):
        return obj.prd.prd_code

    list_display_links = ['item_code', 'title']
    search_fields = ['item_code', 'title']
    ordering = ['-order']

admin.site.register(ItemCommonTB, ItemCommonTBAdmin)


class ItemSubTBAdmin(admin.ModelAdmin):
    list_display = ['prd_name', 'prd_code', 'item_code', 'title' , 'order'] # 커스터마이징 코드

    def prd_name(self, obj):
        return obj.prd.title

    def prd_code(self, obj):
        return obj.prd.prd_code

    list_display_links = ['item_code', 'title']
    search_fields = ['item_code', 'title']
    ordering = ['-order']

admin.site.register(ItemSubTB, ItemSubTBAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'title', 'order'] # 커스터마이징 코드

    def get_name(self, obj):
        return obj.prd.prd_code

    get_name.short_description = 'prd code'  # Renames column

    list_display_links = ['title']
    search_fields = ['title']
    ordering = ['-order']

admin.site.register(ItemTB, ItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_idx', 'user_id', 'get_name', 'count', 'order_time', 'dbstat'] # 커스터마이징 코드

    def get_name(self, obj):
        return obj.prd.prd_code

    get_name.short_description = 'prd code'  # Renames column head

    list_filter = ['order_time', 'dbstat']
    list_display_links = ['order_idx','user_id']
    search_fields = ['user_id']

admin.site.register(OrderTB, OrderAdmin)

class UserStatusAdmin(admin.ModelAdmin):
    list_display = ['userStatus_idx', 'userStatus', 'dbstat']

    list_display_links = ['userStatus']
    search_fields = ['userStatus']


admin.site.register(UserStatusTB, UserStatusAdmin)


class PayAdmin(admin.ModelAdmin):
    list_display = ['pay_idx', 'pay_num', 'get_name', 'prd_info', 'prd_total_price', 'pay_result', 'pay_time'] # 커스터마이징 코드

    list_filter = ['pay_time', 'pay_result']

    def get_name(self, obj):
        if obj.pay_user is not None:
            return obj.pay_user.regi_email
    get_name.short_description = 'pay_user'  # Renames column head

    list_display_links = ['pay_num']
    search_fields = ['pay_num']
    ordering = ['-pay_idx']

admin.site.register(PayTB, PayAdmin)


class MyClassListAdmin(admin.ModelAdmin):
    list_display = ['myclassList_idx', 'pay_num', 'user_id', 'get_name', 'start_time', 'expire_time', 'dbstat'] # 커스터마이징 코드

    list_filter = ['start_time', 'expire_time','dbstat']
    def get_name(self, obj):
        return obj.prd.prd_code

    get_name.short_description = 'prd code'  # Renames column head

    list_display_links = ['user_id']
    search_fields = ['user_id', 'pay_num']

admin.site.register(MyClassListTB, MyClassListAdmin)

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

class statAdmin(admin.ModelAdmin):
    list_display = ['register_cnt', 'login_cnt', 'pay_suc_cnt', 'pay_fail_cnt', 'pre_pay_cnt', 'expire_cnt', 'stime']  # 커스터마이징 코드
    list_filter = ['stime']

admin.site.register(statTB, statAdmin)

admin.site.register(danal_confirmTB)
admin.site.register(runcodingTB)

class couponAdmin(admin.ModelAdmin):
    list_display = ['coupon_num', 'coupon_name', 'delivery_price', 'period', 'discount','expire']  # 커스터마이징 코드

    list_filter = ['expire']

    def get_code(self, obj):
        return obj.prd.prd_code

    get_code.short_description = 'prd_code'  # Renames column head

    list_display_links = ['coupon_num','coupon_name' ]
    search_fields = ['coupon_num']
    ordering = ['-coupon_idx']

admin.site.register(couponTB, couponAdmin)

class myCouponAdmin(admin.ModelAdmin):
    list_display = ['myCoupon_idx', 'get_id', 'get_coupon', 'used','expire', 'dbstat']  # 커스터마이징 코드

    list_filter = ['used', 'expire', 'dbstat']

    def get_id(self, obj):
        return obj.user.regi_email

    get_id.short_description = 'user'  # Renames column head

    def get_coupon(self, obj):
        return obj.coupon.coupon_num

    get_coupon.short_description = 'coupon'  # Renames column head

    list_display_links = ['myCoupon_idx', 'expire']
    search_fields = ['get_id', 'get_coupon']
    ordering = ['-myCoupon_idx']

admin.site.register(myCouponTB, myCouponAdmin)

class PayWayAdmin(admin.ModelAdmin):
    list_display = ['payWay_idx', 'name', 'value', 'dbstat'] # 커스터마이징 코드

    list_filter = ['dbstat']
    list_display_links = ['name', 'value']
    search_fields = ['name', 'value']

admin.site.register(PayWayTB, PayWayAdmin)


admin.site.register(refundTB)