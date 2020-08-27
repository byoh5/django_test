from django.db import models

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
    stime = models.DateTimeField(null=True)
    expireTime = models.DateTimeField(null=True)
    dbstat = models.CharField(max_length=50, default='A')

class LoginTB(models.Model):
    login_idx = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50, default = '') #RegisterTB.regi_id
    session_id = models.CharField(max_length=150)
    login_time = models.DateTimeField(null=True)
    logout_time = models.DateTimeField(null=True)
    dbstat = models.CharField(max_length=50, default='A')

class PrdTB(models.Model):
    prd_idx = models.AutoField(primary_key=True)
    prd_code = models.CharField(max_length=50, default = '')
    title = models.CharField(max_length=50)
    img = models.CharField(max_length=50)
    period = models.IntegerField(null=True)
    class_count = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    option = models.CharField(max_length=50)
    goal = models.CharField(max_length=150)
    url = models.CharField(max_length=50, default = '')
    dbstat = models.CharField(max_length=50, default='A')

class ItemTB(models.Model): #curriculum
    item_idx = models.AutoField(primary_key=True)
    prd = models.ForeignKey(PrdTB, on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    time = models.CharField(max_length=50)

class OrderTB(models.Model):
    order_idx = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50, default = '') #LoginTB.euser_id
    prd_code = models.CharField(max_length=50, default = '') #prdTB.prd_code
    prd = models.ForeignKey(PrdTB, on_delete=models.PROTECT, null=True)
    count = models.IntegerField(default='1')
    delivery = models.CharField(max_length=50, default='기본배송')
    delivery_price = models.IntegerField(default='3000')
    order_time = models.DateTimeField(null=True)