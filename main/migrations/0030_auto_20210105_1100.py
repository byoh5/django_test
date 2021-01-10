# Generated by Django 3.1 on 2021-01-05 02:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20210104_2125'),
    ]

    operations = [
        migrations.CreateModel(
            name='stat_menu',
            fields=[
                ('stat_menu_idx', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=50)),
                ('main_menu', models.CharField(blank=True, default='', max_length=50)),
                ('sub_menu', models.CharField(blank=True, default='', max_length=50)),
                ('search_title', models.CharField(blank=True, default='', max_length=150)),
                ('stime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterField(
            model_name='stat_class',
            name='pay_email',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]