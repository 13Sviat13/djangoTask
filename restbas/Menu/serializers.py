from rest_framework import serializers
from restbas.models import Menu, MenuItem


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['date']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price']
