#!/usr/bin/python3
#coding:utf-8

from rest_framework import serializers
from .models import Server,NetworkDevice,IP
from manufacturer.models import Manufacturer,ProductModel


class ServerAutoReportSerializer(serializers.Serializer):
    """
    服务器同步序列化类.
    这个地方的验证属于程序级别的验证.model是数据库级别的验证,能让程序验证的,就不要进数据库验证.
    """
    ip            =    serializers.IPAddressField(required=True)
    hostname      =    serializers.CharField(required=True,max_length=20)
    cpu           =    serializers.CharField(required=True,max_length=50)
    mem           =    serializers.CharField(required=True,max_length=20)
    disk          =    serializers.CharField(required=True,max_length=200)
    os            =    serializers.CharField(required=True,max_length=50)
    sn            =    serializers.CharField(required=True,max_length=50)
    # manufacturer  =    serializers.PrimaryKeyRelatedField(many=False,queryset=Manufacturer.objects.all())
    manufacturer  =    serializers.CharField(required=True)
    model_name    =    serializers.CharField(required=True)
    uuid          =    serializers.CharField(required=True,max_length=50)
    # network关联对象,接收的时候传一个json格式的数据,然后再处理
    network       =    serializers.JSONField(required=True)

    # 验证1,验证制造商字段manufacturer
    def validate_manufacturer(self, value):
        try: #检查是否存在
            return Manufacturer.objects.get(vendor_name__exact=value)
        except Manufacturer.DoesNotExist:
            # 没有就创建,定义个创建的方法create_manufacturer,返回一个制造商的实例
            return self.create_manufacturer(value)
    # 验证2,
    def validate(self, attrs):
        # network = attrs["network"]
        # del attrs["network"] #取到,然后删掉. 因为数据库里没有这个字段,后面验证会报错
        manufacturer_obj = attrs["manufacturer"]
        try:
            attrs["model_name"] = manufacturer_obj.productmodel_set.get(model_name__exact=attrs["model_name"])
        except ProductModel.DoesNotExist:
            # 创建模型
            attrs["model_name"] = self.create_product_model(manufacturer_obj,attrs["model_name"])
        return attrs

    # 创建时是验证之后的数据
    def create(self, validated_data):
        # network_queryset = validated_data.pop("network") # 删除network,然后将值返回
        network = validated_data.pop("network") # 删除network,然后将值返回
        server_obj = Server.objects.create(**validated_data) # 创建一个server记录
        # server_obj.networkdevice_set = network_queryset # 一对多关联
        self.check_server_network_device(server_obj,network)
        return server_obj

    def check_server_network_device(self,server_obj,network):
        """
        检查此服务器有没有这些网卡设备,并做关联
        """
        network_device_queryset = server_obj.networkdevice_set.all()
        for device in network:
            try:
                network_device_obj = network_device_queryset.get(name__exact=device["name"])
            except NetworkDevice.DoesNotExist:
                # 网卡不存在,创建网卡,定义create_network_device
                self.create_network_device(server_obj,device)

    def check_ip(self,network_device_obj,ifnets):
        # 拿到网卡的所有ip,检查ip在不在网卡上.不存在就创建ip,定义create_ip
        ip_queryset = network_device_obj.ip_set.all()
        for ifnet in ifnets:
            try:
                ip_queryset.get(ifnet["ip_addr"])
            except IP.DoesNotExist:
                ip_obj = self.create_ip(network_device_obj,ifnet)

    def create_ip(self,network_device_obj,ifnet):
        ifnet["device"] = network_device_obj #ip所在的网卡
        return IP.objects.create(**ifnet)

    # 创建网卡,然后检查ip,定义check_ip
    def create_network_device(self,server_obj,device):
        ips = device.pop("ips")
        device["host"] = server_obj #网卡所在的主机
        network_device_obj = NetworkDevice.objects.create(**device)
        self.check_ip(network_device_obj,ips)
        return network_device_obj


    # 创建制造商对象
    def create_manufacturer(self,vendor_name):
        return Manufacturer.objects.create(vendor_name=vendor_name)
    # 创建模型对象

    def create_product_model(self,manufacturer_obj,model_name):
        return ProductModel.objects.create(model_name=model_name,vendor=manufacturer_obj)

    def to_representation(self, instance):
        ret = {
            "hostname":instance.hostname,
            "ip":instance.ip
        }
        return ret

# class ServerSerializer(serializers.ModelSerializer):
class ServerSerializer(serializers.HyperlinkedModelSerializer):
    """服务器序列化类"""
    class Meta:
        model = Server
        fields = "__all__"


class NetworkDeviceSerializer(serializers.ModelSerializer):
    """
    网卡序列化
    """
    class Meta:
        model = NetworkDevice
        fields = "__all__"

class IPSerializer(serializers.ModelSerializer):
    """
    IP序列化
    """
    class Meta:
        model = IP
        fields = "__all__"

