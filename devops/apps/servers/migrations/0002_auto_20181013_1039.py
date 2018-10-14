# Generated by Django 2.0.9 on 2018-10-13 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='model_name',
            field=models.ForeignKey(help_text='服务器型号', on_delete=django.db.models.deletion.CASCADE, to='manufacturer.ProductModel', verbose_name='服务器型号'),
        ),
        migrations.AlterField(
            model_name='server',
            name='rmt_card_ip',
            field=models.CharField(db_index=True, help_text='远程管理卡ip', max_length=15, unique=True, verbose_name='远程管理卡ip'),
        ),
        migrations.AlterField(
            model_name='server',
            name='uuid',
            field=models.CharField(db_index=True, help_text='UUID', max_length=50, unique=True, verbose_name='UUID'),
        ),
    ]
