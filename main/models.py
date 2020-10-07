from django.db import models
from django.utils import timezone
# Create your models here.

class RegisterTB(models.Model):
    regi_idx = models.AutoField(primary_key=True)
    regi_email = models.CharField(max_length=50)
    regi_name = models.CharField(max_length=50)
    regi_phone = models.CharField(max_length=50)
    regi_receiver1_add01 = models.CharField(max_length=50)
    regi_receiver1_add02 = models.CharField(max_length=50)
    regi_receiver1_add03 = models.CharField(max_length=50)
    regi_receiver2_name = models.CharField(max_length=50, default='', blank=True)
    regi_receiver2_phone = models.CharField(max_length=50, default='', blank=True)
    regi_receiver2_add01 = models.CharField(max_length=50, default='', blank=True)
    regi_receiver2_add02 = models.CharField(max_length=50, default='', blank=True)
    regi_receiver2_add03 = models.CharField(max_length=50, default='', blank=True)
    regi_pass = models.CharField(max_length=150)
    level = models.IntegerField(default=0)
    imp_birth = models.CharField(max_length=50, default='', blank=True)
    imp_gender = models.CharField(max_length=50, default='', blank=True)
    stime = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True, blank=True)
    dbstat = models.CharField(max_length=50, default='A')

class LoginTB(models.Model):
    login_idx = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50, default='') #RegisterTB.regi_email
    session_id = models.CharField(max_length=150)
    login_time = models.DateTimeField(default=timezone.now)
    logout_time = models.DateTimeField(null=True)
    stime = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True, blank=True)
    dbstat = models.CharField(max_length=50, default='A')

class PrdTB(models.Model):
    prd_idx = models.AutoField(primary_key=True)
    prd_code = models.CharField(max_length=50, default='') #year(2020) + month(08) + arduino(001), mblock(002), AI(300), kit count(1)
    title = models.CharField(max_length=50)
    title2 = models.CharField(max_length=50, default='') #detail page title
    title3 = models.CharField(max_length=50, default='') #detail sub page title
    img = models.CharField(max_length=50, default='')
    gif = models.CharField(max_length=50, default='')
    period = models.IntegerField(default='0')
    class_count = models.IntegerField(default='0')
    price = models.IntegerField(default='0')
    option1 = models.CharField(max_length=50, blank=True)
    option1_price = models.IntegerField(null=True, blank=True)
    option2 = models.CharField(max_length=50, blank=True)
    option2_price = models.IntegerField(null=True, blank=True)
    option3 = models.CharField(max_length=50, blank=True)
    option3_price = models.IntegerField(null=True, blank=True)
    goal = models.CharField(max_length=150)
    keyword = models.CharField(max_length=50, default = '') #search 용
    stime = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True, blank=True)
    dbstat = models.CharField(max_length=50, default='A')

class ItemDowndataTB(models.Model):
    downdata_idx = models.AutoField(primary_key=True)
    downdata = models.CharField(max_length=50, default='')
    downdata_name = models.CharField(max_length=50, default='')
    prd_code = models.CharField(max_length=50, default='')
    stime = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True, blank=True)
    dbstat = models.CharField(max_length=50, default='A')


class ItemTB(models.Model): #curriculum
    item_idx = models.AutoField(primary_key=True)
    prd = models.ForeignKey(PrdTB, on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    data = models.CharField(max_length=150, default='')
    order = models.IntegerField(default='0')
    stime = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True, blank=True)

class PayWayTB(models.Model):
    payWay_idx = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    dbstat = models.CharField(max_length=50, default='A')

class OrderTB(models.Model):
    order_idx = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50, default = '') #LoginTB.euser_id
    prd = models.ForeignKey(PrdTB, on_delete=models.PROTECT, null=True) #개월 기준
    count = models.IntegerField(default='1')
    pay_num = models.CharField(max_length=50, default='', blank=True)
    option1_selectNum = models.IntegerField(default='0', blank=True)
    option2_selectNum = models.IntegerField(default='0', blank=True)
    option3_selectNum = models.IntegerField(default='0', blank=True)
    delivery = models.CharField(max_length=50, default='기본배송')
    delivery_price = models.IntegerField(default='3000')
    delevery_addr_num = models.IntegerField(default='0')
    order_time = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True, blank=True)
    dbstat = models.CharField(max_length=50, default='A')

class UserStatusTB(models.Model):
    userStatus_idx = models.AutoField(primary_key=True)
    userStatus = models.CharField(max_length=500, default='4')
    dbstat = models.CharField(max_length=50, default='A')
    stime = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True, blank=True)

class MyClassListTB(models.Model):
    myclassList_idx = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50)
    pay_num = models.CharField(max_length=50, default='')
    prd = models.ForeignKey(PrdTB, on_delete=models.PROTECT, null=True)
    dbstat = models.CharField(max_length=50, default='A')
    start_time = models.DateTimeField(default=timezone.now)
    expire_time = models.DateTimeField(default='')
    modified = models.DateTimeField(auto_now=True, blank=True)

class loungeListTB(models.Model):
    loungeList_idx = models.AutoField(primary_key=True)
    img = models.CharField(max_length=150) #preview
    title = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    data_name = models.CharField(max_length=50, default='') #directory name
    description = models.CharField(max_length=50, default='', blank=True)
    video_id = models.CharField(max_length=150, default='')
    dbstat = models.CharField(max_length=50, default='A')
    stime = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True, blank=True)

class categoryTB(models.Model):
    category_idx = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='')
    dbstat = models.CharField(max_length=50, default='A')
    stime = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True, blank=True)

class comunityTB(models.Model):
    comunity_idx = models.AutoField(primary_key=True)
    label_name = models.CharField(max_length=50, default='') # 페이지에서 title과 des를 연결해줄 이름
    category = models.ForeignKey(categoryTB, on_delete=models.PROTECT, default='', blank=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    sub_description1 = models.CharField(max_length=500, default='', blank=True)
    sub_description2 = models.CharField(max_length=500, default='', blank=True)
    dbstat = models.CharField(max_length=50, default='A')
    stime = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True, blank=True)

class statTB(models.Model):
    stat_idx = models.AutoField(primary_key=True)
    register_cnt = models.IntegerField(default='0')
    login_cnt = models.IntegerField(default='0')
    pay_suc_cnt = models.IntegerField(default='0')
    pay_fail_cnt = models.IntegerField(default='0')
    pre_pay_cnt = models.IntegerField(default='0')
    expire_cnt = models.IntegerField(default='0')
    stime = models.DateTimeField(default=timezone.now)

class danal_confirmTB(models.Model):
    confirm_idx = models.AutoField(primary_key=True)
    imp_uid = models.CharField(max_length=150)
    regi_user = models.ForeignKey(RegisterTB, on_delete=models.PROTECT, default='', blank=True)
    imp_name = models.CharField(max_length=50, default='', blank=True)
    access_token = models.CharField(max_length=150)
    new_phone = models.CharField(max_length=50, default='', blank=True)
    stime = models.DateTimeField(default=timezone.now)
    dbstat = models.CharField(max_length=50, default='A')

class runcodingTB(models.Model):
    runcoding_idx = models.AutoField(primary_key=True)
    mail = models.CharField(max_length=50)
    mail_pass = models.CharField(max_length=150)
    mail_port = models.CharField(max_length=50)
    imp_key = models.CharField(max_length=150)
    imp_secret = models.CharField(max_length=300)

class couponTB(models.Model):
    coupon_idx = models.AutoField(primary_key=True)
    coupon_num = models.CharField(max_length=150, unique=True)
    coupon_name = models.CharField(max_length=150, default='')
    delivery_price = models.BooleanField(default=False) #False:배송비무료 , True:기존정책
    discount = models.IntegerField(default='0', blank=True)
    prd = models.ForeignKey(PrdTB, on_delete=models.PROTECT, default='', blank=True, null=True)
    period = models.IntegerField(default='1', null=True) # 쿠폰 사용의 유효기간 (사용자마다 몇개월 안에 사용 )
    expire = models.DateTimeField(default='') # 쿠폰 등록의 유효기간
    dbstat = models.CharField(max_length=50, default='A')

class myCouponTB(models.Model):
    myCoupon_idx = models.AutoField(primary_key=True)
    user = models.ForeignKey(RegisterTB, on_delete=models.PROTECT, default='')
    coupon = models.ForeignKey(couponTB, on_delete=models.PROTECT, default='')
    used = models.BooleanField(default=False)
    dbstat = models.CharField(max_length=50, default='A')
    expire = models.DateTimeField(default='')
    stime = models.DateTimeField(default=timezone.now)

class PayTB(models.Model):
    pay_idx = models.AutoField(primary_key=True)
    pay_num = models.CharField(max_length=50, default='')
    pay_user = models.ForeignKey(RegisterTB, on_delete=models.PROTECT, null=True)
    pay_user_status = models.ForeignKey(UserStatusTB, on_delete=models.PROTECT, null=True)
    order_id = models.CharField(max_length=50, default='') #order_idx
    payWay = models.ForeignKey(PayWayTB, on_delete=models.PROTECT, null=True)
    payWay_deposit_name = models.CharField(max_length=50, default='',blank=True)
    payWay_deposit_receipt = models.CharField(max_length=10, default='D')
    coupon_num = models.CharField(max_length=150, default='', null=True)
    prd_info = models.CharField(max_length=150, default='') #prd 제목 외 몇개
    prd_price = models.IntegerField(default='0') # product total
    delivery_price = models.IntegerField(default='0')
    prd_total_price = models.IntegerField(default='0')  # product total + delivary
    delivery_name = models.CharField(max_length=50, default='')
    delivery_addr = models.CharField(max_length=150, default='')
    delivery_phone = models.CharField(max_length=50, default='')
    pay_result = models.IntegerField(default='100') # 0: 결제성공 1: 결제실패
    pay_result_info = models.CharField(max_length=500, default='') #pay_msg
    pay_time = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True, blank=True)