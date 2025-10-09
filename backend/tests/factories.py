from decimal import Decimal
from django.utils import timezone
from menu_app.models import (
    Restaurant, Menu, MenuSection, MenuItem,
    DietaryRestriction, ProcessingLog
)

def make_restaurant(name="Test Restaurant", location="Madrid, Spain"):
    # matches: restaurant(name, location)
    return Restaurant.objects.create(name=name, location=location)

def make_menu(restaurant=None, version=1, date=None):
    # matches: menu(restaurant_id, version, date)
    restaurant = restaurant or make_restaurant()
    return Menu.objects.create(
        restaurant=restaurant,
        version=version,
        date=date or timezone.now().date()
    )

def make_section(menu=None, section_name="Appetizers", section_order=1):
    # matches: menusection(section_name, section_order)
    menu = menu or make_menu()
    return MenuSection.objects.create(
        menu=menu,
        section_name=section_name,
        section_order=section_order
    )

def make_dietary_restriction(label="Vegetarian"):
    # matches: dietaryrestriction(label)
    return DietaryRestriction.objects.create(label=label)

def make_item(
    section=None,
    name="Bruschetta",
    description="Grilled bread with tomatoes",
    price="8.50",
    dietary_restriction=None,
):
    # matches: menuitem(name, description, price, dietary_restriction_id)
    section = section or make_section()
    if dietary_restriction is False:  # allow explicitly “no restriction”
        dietary_restriction = None
    return MenuItem.objects.create(
        section=section,
        name=name,
        description=description,
        price=Decimal(price),
        dietary_restriction=dietary_restriction
    )

def make_processing_log(menu=None, status="SUCCESS", error_message=""):
    # matches: processinglog(menu_id, status, error_message, timestamp)
    menu = menu or make_menu()
    return ProcessingLog.objects.create(
        menu=menu,
        status=status,
        error_message=error_message,
        timestamp=timezone.now()
    )
