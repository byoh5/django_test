# Generated by Django 3.1 on 2020-12-11 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20201211_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemcommontb',
            name='downdata',
        ),
        migrations.RemoveField(
            model_name='itemcommontb',
            name='downdata_name',
        ),
        migrations.RemoveField(
            model_name='itemsubtb',
            name='downdata',
        ),
        migrations.RemoveField(
            model_name='itemsubtb',
            name='downdata_name',
        ),
        migrations.RemoveField(
            model_name='itemtb',
            name='downdata',
        ),
        migrations.RemoveField(
            model_name='itemtb',
            name='downdata_name',
        ),
        migrations.AddField(
            model_name='itemsubtb',
            name='iteminfo_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemInfoTB_Sub_1', to='main.iteminfotb'),
        ),
        migrations.AddField(
            model_name='itemsubtb',
            name='iteminfo_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemInfoTB_Sub_2', to='main.iteminfotb'),
        ),
        migrations.AddField(
            model_name='itemsubtb',
            name='iteminfo_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemInfoTB_Sub_3', to='main.iteminfotb'),
        ),
        migrations.AddField(
            model_name='itemsubtb',
            name='iteminfo_4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemInfoTB_Sub_4', to='main.iteminfotb'),
        ),
        migrations.AddField(
            model_name='itemsubtb',
            name='iteminfo_5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemInfoTB_Sub_5', to='main.iteminfotb'),
        ),
        migrations.AddField(
            model_name='itemtb',
            name='iteminfo_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemInfoTB_1', to='main.iteminfotb'),
        ),
        migrations.AddField(
            model_name='itemtb',
            name='iteminfo_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemInfoTB_2', to='main.iteminfotb'),
        ),
        migrations.AddField(
            model_name='itemtb',
            name='iteminfo_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemInfoTB_3', to='main.iteminfotb'),
        ),
        migrations.AddField(
            model_name='itemtb',
            name='iteminfo_4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemInfoTB_4', to='main.iteminfotb'),
        ),
        migrations.AddField(
            model_name='itemtb',
            name='iteminfo_5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemInfoTB_5', to='main.iteminfotb'),
        ),
        migrations.AlterField(
            model_name='itemcommontb',
            name='iteminfo_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemInfoTB_Common_1', to='main.iteminfotb'),
        ),
        migrations.AlterField(
            model_name='itemcommontb',
            name='iteminfo_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemInfoTB_Common_2', to='main.iteminfotb'),
        ),
        migrations.AlterField(
            model_name='itemcommontb',
            name='iteminfo_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemInfoTB_Common_3', to='main.iteminfotb'),
        ),
        migrations.AlterField(
            model_name='itemcommontb',
            name='iteminfo_4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemInfoTB_Common_4', to='main.iteminfotb'),
        ),
        migrations.AlterField(
            model_name='itemcommontb',
            name='iteminfo_5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ItemInfoTB_Common_5', to='main.iteminfotb'),
        ),
    ]
