from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Restaurant, Menu, MenuSection, MenuItem, DietaryRestriction, ProcessingLog

@admin.register(Restaurant)
class RestaurantAdmin(ModelAdmin):
   list_display = ('name', 'location')
   search_fields = ('name',)

@admin.register(Menu)
class MenuAdmin(ModelAdmin):
   list_display = ('restaurant', 'version', 'date')
   list_filter = ('restaurant', 'date')

@admin.register(MenuSection)
class MenuSectionAdmin(ModelAdmin):
   list_display = ('menu', 'section_name', 'section_order')
   list_filter = ('menu',)

@admin.register(MenuItem)
class MenuItemAdmin(ModelAdmin):
   list_display = ('name', 'section', 'price', 'dietary_restriction')
   list_filter = ('section', 'dietary_restriction')

@admin.register(DietaryRestriction)
class DietaryRestrictionAdmin(ModelAdmin):
   list_display = ('label',)
   search_fields = ('label',)

@admin.register(ProcessingLog)
class ProcessingLogAdmin(ModelAdmin):
   list_display = ('menu', 'status', 'timestamp')
   list_filter = ('status', 'timestamp')