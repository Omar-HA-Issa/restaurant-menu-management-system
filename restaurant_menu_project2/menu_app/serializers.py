from rest_framework import serializers
from .models import Restaurant, Menu, MenuSection, MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class MenuSectionSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)
    class Meta:
        model = MenuSection
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    sections = MenuSectionSerializer(many=True, read_only=True)
    class Meta:
        model = Menu
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(many=True, read_only=True)
    class Meta:
        model = Restaurant
        fields = '__all__'

