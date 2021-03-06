#!/usr/bin/python3
#coding:utf-8

from rest_framework import serializers
from django.contrib.auth.models import Permission, ContentType


# class ContentTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ContentType
#         fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    # content_type = ContentTypeSerializer() 最简单的方式,指定字段content_type

    def to_representation(self, instance):
        # 需要指定 content_type
        # ret = super(PermissionSerializer,self).to_representation(instance) 自定义字段,不要父类的ret数据了
        ret = {}
        ret["key"] = instance.id
        ret["label"] = "{}.{}".format(instance.content_type.app_label, instance.codename)
        return ret

    class Meta:
        model = Permission
        fields = "__all__"


