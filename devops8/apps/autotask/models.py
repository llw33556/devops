#!/usr/bin/python
#coding:utf-8

from django.db import models


class Tasks(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'任务名称')
    # django文件上传字段FileField,upload_to指上传文件的位置,会在项目根目录生成playbook目录存放文件
    playbook = models.FileField(upload_to='playbook/%Y/%m', verbose_name=u'playbook文件')
    # 执行结果字段TextField
    detail_result = models.TextField(verbose_name=u'执行结果详情', null=True, blank=True)
    status = models.CharField(max_length=1, choices=(('Y', '已执行'), ('N', '未执行')), default='N', verbose_name=u'执行状态')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'任务创建时间')
    exec_time = models.DateTimeField(auto_now=True, verbose_name=u'执行时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '任务'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']


