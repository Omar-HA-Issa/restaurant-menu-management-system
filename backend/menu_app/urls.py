from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import RestaurantViewSet, MenuViewSet, MenuItemViewSet, analytics_views

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menus', MenuViewSet)
router.register(r'menuitems', MenuItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/analytics/', analytics_views, name='analytics_views'),
    path('upload-menu/', views.menu_upload_view, name='menu_upload'),
    path('process-menu-pdf/', views.process_menu_pdf, name='process_menu_pdf'),
]