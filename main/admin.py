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

class codingkit_category_largeAdmin(admin.ModelAdmin):
    list_display = ['codingkit_category_large_idx', 'name', 'dbstat'] # 커스터마이징 코드
    list_display_links = ['name']
    list_filter = ['name', 'dbstat']

    search_fields = ['name', 'dbstat']

admin.site.register(codingkit_category_large, codingkit_category_largeAdmin)

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

class ItemSubKitTBAdmin(admin.ModelAdmin):
    list_display = ['ItemSubKit_idx', 'prd_name', 'prd_code', 'item_code', 'title', 'description'] # 커스터마이징 코드

    def prd_name(self, obj):
        return obj.prd.title

    def prd_code(self, obj):
        return obj.prd.prd_code

    list_display_links = ['item_code', 'title', 'description']
    search_fields = ['item_code', 'title', 'description']

admin.site.register(ItemSubKitTB, ItemSubKitTBAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'title', 'order'] # 커스터마이징 코드

    def get_name(self, obj):
        return obj.prd.prd_code

    get_name.short_description = 'prd code'  # Renames column

    list_display_links = ['title']
    search_fields = ['title']
    ordering = ['-order']

admin.site.register(ItemTB, ItemAdmin)

class BonusItemTBAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'title', 'subTitle', 'order'] # 커스터마이징 코드

    def get_name(self, obj):
        return obj.prd.bonus_prdCode

    get_name.short_description = 'prd code'  # Renames column

    list_display_links = ['title', 'subTitle']
    search_fields = ['title', 'subTitle']
    ordering = ['-order']

admin.site.register(BonusItemTB, BonusItemTBAdmin)

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
    list_display = ['myclassList_idx', 'pay_num', 'user_id', 'item_code', 'start_time', 'expire_time', 'dbstat'] # 커스터마이징 코드

    list_filter = ['dbstat', 'item_code']

    list_display_links = ['user_id','item_code']
    search_fields = ['user_id', 'pay_num','item_code']

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
admin.site.register(runcoding_bizTB)

class couponAdmin(admin.ModelAdmin):
    list_display = ['coupon_num', 'coupon_name', 'delivery_price', 'period', 'discount','expire', 'dbstat']  # 커스터마이징 코드

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

class refundTBAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'user_email', 'prd_title', 'pay_way', 'refund_time', 'dbstat'] # 커스터마이징 코드

    list_filter = ['dbstat']
    list_display_links = ['user_name', 'user_email', 'prd_title']
    search_fields = ['user_name', 'user_email', 'prd_title', 'pay_way']

admin.site.register(refundTB, refundTBAdmin)


class stat_classAdmin(admin.ModelAdmin):
    list_display = ['pay_email', 'item_code', 'class_title', 'class_data', 'stime'] # 커스터마이징 코드

    list_filter = ['item_code', 'class_title']
    list_display_links = ['pay_email', 'item_code', 'class_title']
    search_fields = ['pay_email', 'item_code', 'class_title', 'class_data']

admin.site.register(stat_class, stat_classAdmin)

class stat_menuAdmin(admin.ModelAdmin):
    list_display = ['user', 'main_menu', 'sub_menu', 'info_search_etc', 'stime'] # 커스터마이징 코드

    list_filter = ['main_menu']
    list_display_links = ['user', 'main_menu']
    search_fields = ['user', 'main_menu', 'sub_menu', 'info_search_etc', 'stime']

admin.site.register(stat_menu, stat_menuAdmin)

class bonus_prdAdmin(admin.ModelAdmin):
    list_display = ['target1_name', 'target2_name', 'bonus_prdCode', 'dbstat'] # 커스터마이징 코드

    def target1_name(self, obj):
        return obj.targetPrd_1.title

    def target2_name(self, obj):
        return obj.targetPrd_2.title

    list_filter = ['dbstat']
    list_display_links = ['bonus_prdCode', 'dbstat']
    search_fields = ['target1_name', 'target2_name', 'bonus_prdCode', 'dbstat']

admin.site.register(bonus_prd, bonus_prdAdmin)


class popupAdmin(admin.ModelAdmin):
    list_display = ['img', 'text', 'link', 'btn_img', 'expire_time', 'dbstat'] # 커스터마이징 코드

    list_filter = ['dbstat']
    list_display_links = ['img', 'text', 'link', 'btn_img']
    search_fields = ['img', 'text', 'link', 'dbstat']

admin.site.register(popup, popupAdmin)