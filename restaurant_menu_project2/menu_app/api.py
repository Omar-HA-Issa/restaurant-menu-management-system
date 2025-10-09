from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Restaurant, Menu, MenuItem
from .serializers import RestaurantSerializer, MenuSerializer, MenuItemSerializer
from .views_queries import (
    get_menu_items_per_restaurant,
    get_dietary_restrictions_distribution,
    get_price_analysis
)

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

@api_view(['GET'])
def analytics_views(request):
    return Response({
        'menu_items_per_restaurant': get_menu_items_per_restaurant(),
        'dietary_restrictions': get_dietary_restrictions_distribution(),
        'price_analysis': get_price_analysis()
    })