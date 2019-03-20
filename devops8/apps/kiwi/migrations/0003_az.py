# Generated by Django 2.1.7 on 2019-03-16 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kiwi', '0002_auto_20190315_2230'),
    ]

    operations = [
        migrations.CreateModel(
            name='AZ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='AZ', max_length=30, verbose_name='AZ')),
                ('remark', models.CharField(help_text='备注', max_length=200, null=True, verbose_name='备注')),
                ('idc', models.ForeignKey(help_text='所在Idc', on_delete=django.db.models.deletion.CASCADE, related_name='idc_az', to='kiwi.Idc', verbose_name='所在Idc')),
            ],
            options={
                'verbose_name': 'AZ',
                'verbose_name_plural': 'AZ',
            },
        ),
    ]
