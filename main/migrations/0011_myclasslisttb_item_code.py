# Generated by Django 3.1 on 2020-11-19 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_itemtb_item_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='myclasslisttb',
            name='item_code',
            field=models.CharField(default='', max_length=50),
        ),
    ]