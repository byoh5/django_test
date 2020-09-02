from django.db import models
from django.utils import timezone
# Create your models here.
class RegisterTB(models.Model):
    regi_idx = models.AutoField(primary_key=True)
    regi_id = models.CharField(max_length=50) #가입떄 입력한 ID
    regi_name = models.CharField(max_length=50)
    regi_phone = models.CharField(max_length=50)
    regi_email = models.CharField(max_length=50)
    regi_add01 = models.CharField(max_length=50)
    regi_add02 = models.CharField(max_length=50)
    regi_add03 = models.CharField(max_length=50)
    regi_pass = models.CharField(max_length=50)
    stime = models.DateTimeField(default=timezone.now)
    expireTime = models.DateTimeField(null=True)
    dbstat = models.CharField(max_length=50, default='A')

class LoginTB(models.Model):
    login_idx = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50, default = '') #RegisterTB.regi_id
    session_id = models.CharField(max_length=150)
    login_time = models.DateTimeField(default=timezone.now)
    logout_time = models.DateTimeField(null=True)
    dbstat = models.CharField(max_length=50, default='A')

#kit1 : trashcan
class PrdTB(models.Model):
    prd_idx = models.AutoField(primary_key=True)
    prd_code = models.CharField(max_length=50, default='') #year(2020) + month(08) + arduino(001), mblock(002), AI(300), kit count(1)
    title = models.CharField(max_length=50)
    title2 = models.CharField(max_length=50, default='') #detail page title
    title3 = models.CharField(max_length=50, default='') #detail sub page title
    img = models.CharField(max_length=50)
    period = models.IntegerField(null=True)
    class_count = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    option = models.CharField(max_length=50)
    goal = models.CharField(max_length=150)
    url = models.CharField(max_length=50, default = '')
    dbstat = models.CharField(max_length=50, default='A')

class ItemDowndataTB(models.Model):
    downdata_idx = models.AutoField(primary_key=True)
    downdata = models.CharField(max_length=50, default='')
    downdata_name = models.CharField(max_length=50, default='')
    prd_code = models.CharField(max_length=50, default='')
    dbstat = models.CharField(max_length=50, default='A')


class ItemTB(models.Model): #curriculum
    item_idx = models.AutoField(primary_key=True)
    prd_code = models.CharField(max_length=50, default='')
    prd = models.ForeignKey(PrdTB, on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    data = models.CharField(max_length=150, default='')
    order = models.IntegerField(default='0')

class OrderTB(models.Model):
    order_idx = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50, default = '') #LoginTB.euser_id
    prd_code = models.CharField(max_length=50, default = '') #prdTB.prd_code
    prd = models.ForeignKey(PrdTB, on_delete=models.PROTECT, null=True) #개월 기준
    count = models.IntegerField(default='1')
    delivery = models.CharField(max_length=50, default='기본배송')
    delivery_price = models.IntegerField(default='3000')
    order_time = models.DateTimeField(default=timezone.now)
    dbstat = models.CharField(max_length=50, default='A')

class PayTB(models.Model):
    pay_idx = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50)
    pay_user = models.ForeignKey(RegisterTB, on_delete=models.PROTECT, null=True)
    order_id = models.CharField(max_length=50, default='') #order_idx
    prd_info = models.CharField(max_length=150, default='') #prd 제목 외 몇개
    prd_price = models.IntegerField(default='0') # product total
    delivery_price = models.IntegerField(default='0')
    prd_total_price = models.IntegerField(default='0')  # product total + delivary
    pay_result = models.IntegerField(default='100') # 0: 성공 1: 실패
    pay_result_info = models.CharField(max_length=300, default='') #pay_msg
    pay_time = models.DateTimeField(default=timezone.now)

class MyClassListTB(models.Model):
    myclassList_idx = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50)
    prd = models.ForeignKey(PrdTB, on_delete=models.PROTECT, null=True)
    start_time = models.DateTimeField(default=timezone.now)
    expire_time = models.DateTimeField(default='')
    dbstat = models.CharField(max_length=50, default='A')
