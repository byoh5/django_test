# Generated by Django 3.1 on 2020-11-12 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20201111_1237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prdtb',
            old_name='title3',
            new_name='list',
        ),
        migrations.AddField(
            model_name='prdtb',
            name='tag',
            field=models.CharField(default='', max_length=50),
        ),
    ]