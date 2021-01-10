# Generated by Django 3.1 on 2020-11-10 10:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='categoryTB',
            fields=[
                ('category_idx', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=50)),
                ('dbstat', models.CharField(default='A', max_length=50)),
                ('stime', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='couponTB',
            fields=[
                ('coupon_idx', models.AutoField(primary_key=True, serialize=False)),
                ('coupon_num', models.CharField(max_length=150, unique=True)),
                ('coupon_name', models.CharField(default='', max_length=150)),
                ('delivery_price', models.BooleanField(default=False)),
                ('discount', models.IntegerField(blank=True, default='0')),
                ('period', models.IntegerField(default='1', null=True)),
                ('expire', models.DateTimeField(default='')),
                ('dbstat', models.CharField(default='A', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ItemCommonTB',
            fields=[
                ('itemcommon_idx', models.AutoField(primary_key=True, serialize=False)),
                ('item_code', models.CharField(default='', max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('time', models.CharField(max_length=50)),
                ('data', models.CharField(default='', max_length=150)),
                ('stime', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LoginTB',
            fields=[
                ('login_idx', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(default='', max_length=50)),
                ('session_id', models.CharField(max_length=150)),
                ('login_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('logout_time', models.DateTimeField(null=True)),
                ('stime', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('dbstat', models.CharField(default='A', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='loungeListTB',
            fields=[
                ('loungeList_idx', models.AutoField(primary_key=True, serialize=False)),
                ('img', models.CharField(max_length=150)),
                ('title', models.CharField(max_length=50)),
                ('user', models.CharField(max_length=50)),
                ('data_name', models.CharField(default='', max_length=50)),
                ('description', models.CharField(blank=True, default='', max_length=50)),
                ('video_id', models.CharField(default='', max_length=150)),
                ('dbstat', models.CharField(default='A', max_length=50)),
                ('stime', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PayWayTB',
            fields=[
                ('payWay_idx', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
                ('dbstat', models.CharField(default='A', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PrdTB',
            fields=[
                ('prd_idx', models.AutoField(primary_key=True, serialize=False)),
                ('prd_code', models.CharField(default='', max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('title2', models.CharField(blank=True, default='', max_length=50)),
                ('title3', models.CharField(blank=True, default='', max_length=50)),
                ('img', models.CharField(default='', max_length=50)),
                ('gif', models.CharField(default='', max_length=50)),
                ('period', models.IntegerField(default='0')),
                ('class_count', models.IntegerField(default='0')),
                ('price', models.IntegerField(default='0')),
                ('option1', models.CharField(blank=True, max_length=50)),
                ('option1_price', models.IntegerField(blank=True, null=True)),
                ('option2', models.CharField(blank=True, max_length=50)),
                ('option2_price', models.IntegerField(blank=True, null=True)),
                ('option3', models.CharField(blank=True, max_length=50)),
                ('option3_price', models.IntegerField(blank=True, null=True)),
                ('goal', models.CharField(max_length=150)),
                ('keyword', models.CharField(default='', max_length=50)),
                ('stime', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('dbstat', models.CharField(default='A', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='refundTB',
            fields=[
                ('refund_idx', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(default='', max_length=50)),
                ('user_email', models.CharField(default='', max_length=50)),
                ('user_number', models.CharField(default='', max_length=50)),
                ('pay_num', models.CharField(default='', max_length=50)),
                ('prd_title', models.CharField(max_length=50)),
                ('prd_price', models.IntegerField(default='0')),
                ('option1', models.CharField(blank=True, max_length=50)),
                ('option1_price', models.IntegerField(blank=True, null=True)),
                ('option2', models.CharField(blank=True, max_length=50)),
                ('option2_price', models.IntegerField(blank=True, null=True)),
                ('option3', models.CharField(blank=True, max_length=50)),
                ('option3_price', models.IntegerField(blank=True, null=True)),
                ('refund_price', models.IntegerField(blank=True, null=True)),
                ('prd_total_price', models.IntegerField(default='0')),
                ('delivery_price', models.IntegerField(default='0')),
                ('delivery_name', models.CharField(default='', max_length=50)),
                ('delivery_addr', models.CharField(default='', max_length=150)),
                ('delivery_phone', models.CharField(default='', max_length=50)),
                ('delivery_time', models.DateTimeField(blank=True, null=True)),
                ('pay_time', models.DateTimeField(auto_now=True)),
                ('pay_way', models.CharField(default='', max_length=50)),
                ('payWay_name', models.CharField(blank=True, default='', max_length=50)),
                ('payWay_account', models.CharField(blank=True, default='', max_length=50)),
                ('merchant_uid', models.CharField(blank=True, default='', max_length=500)),
                ('imp_uid', models.CharField(blank=True, default='', max_length=500)),
                ('card_apply', models.CharField(blank=True, default='', max_length=500)),
                ('reason', models.CharField(blank=True, default='', max_length=500)),
                ('card_code', models.CharField(blank=True, default='', max_length=50)),
                ('card_name', models.CharField(blank=True, default='', max_length=50)),
                ('card_number', models.CharField(blank=True, default='', max_length=50)),
                ('card_type', models.CharField(blank=True, default='', max_length=10)),
                ('refund_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('dbstat', models.CharField(default='A', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RegisterTB',
            fields=[
                ('regi_idx', models.AutoField(primary_key=True, serialize=False)),
                ('regi_email', models.CharField(max_length=50)),
                ('regi_name', models.CharField(max_length=50)),
                ('regi_phone', models.CharField(max_length=50)),
                ('regi_receiver1_add01', models.CharField(max_length=50)),
                ('regi_receiver1_add02', models.CharField(max_length=50)),
                ('regi_receiver1_add03', models.CharField(max_length=50)),
                ('regi_receiver2_name', models.CharField(blank=True, default='', max_length=50)),
                ('regi_receiver2_phone', models.CharField(blank=True, default='', max_length=50)),
                ('regi_receiver2_add01', models.CharField(blank=True, default='', max_length=50)),
                ('regi_receiver2_add02', models.CharField(blank=True, default='', max_length=50)),
                ('regi_receiver2_add03', models.CharField(blank=True, default='', max_length=50)),
                ('regi_pass', models.CharField(max_length=150)),
                ('level', models.IntegerField(default=0)),
                ('imp_birth', models.CharField(blank=True, default='', max_length=50)),
                ('imp_gender', models.CharField(blank=True, default='', max_length=50)),
                ('stime', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('dbstat', models.CharField(default='A', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='runcodingTB',
            fields=[
                ('runcoding_idx', models.AutoField(primary_key=True, serialize=False)),
                ('mail', models.CharField(max_length=50)),
                ('mail_pass', models.CharField(max_length=150)),
                ('mail_port', models.CharField(max_length=50)),
                ('imp_key', models.CharField(max_length=150)),
                ('imp_secret', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='statTB',
            fields=[
                ('stat_idx', models.AutoField(primary_key=True, serialize=False)),
                ('register_cnt', models.IntegerField(default='0')),
                ('login_cnt', models.IntegerField(default='0')),
                ('pay_suc_cnt', models.IntegerField(default='0')),
                ('pay_fail_cnt', models.IntegerField(default='0')),
                ('pre_pay_cnt', models.IntegerField(default='0')),
                ('expire_cnt', models.IntegerField(default='0')),
                ('stime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='UserStatusTB',
            fields=[
                ('userStatus_idx', models.AutoField(primary_key=True, serialize=False)),
                ('userStatus', models.CharField(default='4', max_length=500)),
                ('dbstat', models.CharField(default='A', max_length=50)),
                ('stime', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PayTB',
            fields=[
                ('pay_idx', models.AutoField(primary_key=True, serialize=False)),
                ('pay_num', models.CharField(default='', max_length=50)),
                ('pay_email', models.CharField(blank=True, max_length=50, null=True)),
                ('order_id', models.CharField(default='', max_length=50)),
                ('payWay_name', models.CharField(blank=True, default='', max_length=50)),
                ('payWay_receipt', models.CharField(default='D', max_length=10)),
                ('coupon_num', models.CharField(default='', max_length=150, null=True)),
                ('prd_info', models.CharField(default='', max_length=150)),
                ('prd_price', models.IntegerField(default='0')),
                ('delivery_price', models.IntegerField(default='0')),
                ('prd_total_price', models.IntegerField(default='0')),
                ('delivery_name', models.CharField(default='', max_length=50)),
                ('delivery_addr', models.CharField(default='', max_length=150)),
                ('delivery_phone', models.CharField(default='', max_length=50)),
                ('delivery_time', models.DateTimeField(blank=True, null=True)),
                ('pay_result', models.IntegerField(default='100')),
                ('pay_result_info', models.CharField(default='', max_length=500)),
                ('merchant_uid', models.CharField(default='', max_length=500)),
                ('imp_uid', models.CharField(default='', max_length=500)),
                ('card_apply', models.CharField(default='', max_length=500)),
                ('pay_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('payWay', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.paywaytb')),
                ('pay_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.registertb')),
                ('pay_user_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.userstatustb')),
            ],
        ),
        migrations.CreateModel(
            name='OrderTB',
            fields=[
                ('order_idx', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(default='', max_length=50)),
                ('count', models.IntegerField(default='1')),
                ('pay_num', models.CharField(blank=True, default='', max_length=50)),
                ('option1_selectNum', models.IntegerField(blank=True, default='0')),
                ('option2_selectNum', models.IntegerField(blank=True, default='0')),
                ('option3_selectNum', models.IntegerField(blank=True, default='0')),
                ('delivery', models.CharField(default='기본배송', max_length=50)),
                ('delivery_price', models.IntegerField(default='3000')),
                ('delevery_addr_num', models.IntegerField(default='0')),
                ('order_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('dbstat', models.CharField(default='A', max_length=50)),
                ('prd', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.prdtb')),
            ],
        ),
        migrations.CreateModel(
            name='myCouponTB',
            fields=[
                ('myCoupon_idx', models.AutoField(primary_key=True, serialize=False)),
                ('used', models.BooleanField(default=False)),
                ('dbstat', models.CharField(default='A', max_length=50)),
                ('expire', models.DateTimeField(default='')),
                ('stime', models.DateTimeField(default=django.utils.timezone.now)),
                ('coupon', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='main.coupontb')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='main.registertb')),
            ],
        ),
        migrations.CreateModel(
            name='MyClassListTB',
            fields=[
                ('myclassList_idx', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=50)),
                ('pay_num', models.CharField(default='', max_length=50)),
                ('dbstat', models.CharField(default='A', max_length=50)),
                ('play', models.CharField(default='D', max_length=50)),
                ('play_time', models.CharField(blank=True, default='', max_length=50)),
                ('play_video', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('expire_time', models.DateTimeField(default='')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('prd', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.prdtb')),
            ],
        ),
        migrations.CreateModel(
            name='ItemTB',
            fields=[
                ('item_idx', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('time', models.CharField(max_length=50)),
                ('data', models.CharField(default='', max_length=150)),
                ('order', models.IntegerField(blank=True, default='0', null=True)),
                ('downdata', models.CharField(blank=True, max_length=50, null=True)),
                ('downdata_name', models.CharField(blank=True, max_length=50, null=True)),
                ('stime', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('common', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.itemcommontb')),
                ('prd', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.prdtb')),
            ],
        ),
        migrations.CreateModel(
            name='danal_confirmTB',
            fields=[
                ('confirm_idx', models.AutoField(primary_key=True, serialize=False)),
                ('imp_uid', models.CharField(max_length=150)),
                ('imp_name', models.CharField(blank=True, default='', max_length=50)),
                ('access_token', models.CharField(max_length=150)),
                ('new_phone', models.CharField(blank=True, default='', max_length=50)),
                ('stime', models.DateTimeField(default=django.utils.timezone.now)),
                ('dbstat', models.CharField(default='A', max_length=50)),
                ('regi_user', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.PROTECT, to='main.registertb')),
            ],
        ),
        migrations.AddField(
            model_name='coupontb',
            name='prd',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.PROTECT, to='main.prdtb'),
        ),
        migrations.CreateModel(
            name='comunityTB',
            fields=[
                ('comunity_idx', models.AutoField(primary_key=True, serialize=False)),
                ('label_name', models.CharField(default='', max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('sub_description1', models.CharField(blank=True, default='', max_length=500)),
                ('sub_description2', models.CharField(blank=True, default='', max_length=500)),
                ('dbstat', models.CharField(default='A', max_length=50)),
                ('stime', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.PROTECT, to='main.categorytb')),
            ],
        ),
    ]
