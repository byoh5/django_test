# Generated by Django 3.1 on 2020-11-11 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20201110_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemtb',
            name='common',
        ),
        migrations.AddField(
            model_name='itemcommontb',
            name='prd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.prdtb'),
        ),
    ]
