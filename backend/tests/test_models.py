import pytest
from decimal import Decimal

# factories now live in backend/tests/
from tests.factories import (
    make_restaurant,
    make_menu,
    make_section,
    make_item,
    make_dietary_restriction,
    make_processing_log,
)

@pytest.mark.django_db
def test_restaurant_str_is_name():
    r = make_restaurant(name="PizzaPlace")
    assert str(r) == "PizzaPlace"

@pytest.mark.django_db
def test_menu_links_to_restaurant():
    r = make_restaurant(name="Taster")
    m = make_menu(restaurant=r)  # no name kwarg in schema
    assert m.restaurant_id == r.pk

@pytest.mark.django_db
def test_item_links_to_menu_via_section():
    m = make_menu()
    s = make_section(menu=m, section_name="Main", section_order=1)
    item = make_item(section=s)
    assert item.section.menu_id == m.pk
    assert item.section.section_name == "Main"

@pytest.mark.django_db
def test_item_price_stored_correctly():
    item = make_item(price="12.99")
    assert item.price == Decimal("12.99")

@pytest.mark.django_db
def test_menu_versioning():
    m1 = make_menu(version=1)
    m2 = make_menu(version=2, restaurant=m1.restaurant)
    assert m1.version == 1 and m2.version == 2

# --- ADDITIONAL TESTS BELOW ---

@pytest.mark.django_db
def test_item_with_dietary_restriction_links():
    s = make_section()
    veg = make_dietary_restriction(label="Vegetarian")
    item = make_item(section=s, name="Veg Pizza", price="9.50", dietary_restriction=veg)
    assert item.dietary_restriction_id == veg.pk

@pytest.mark.django_db
def test_sections_return_in_order():
    m = make_menu()
    make_section(menu=m, section_name="Mains", section_order=2)
    make_section(menu=m, section_name="Starters", section_order=1)
    names = list(
        m.menusection_set.order_by("section_order").values_list("section_name", flat=True)
    )
    assert names == ["Starters", "Mains"]

@pytest.mark.django_db
def test_processing_log_persists_status_and_timestamp():
    m = make_menu()
    log = make_processing_log(menu=m, status="SUCCESS", error_message="")
    assert log.menu_id == m.pk
    assert log.status == "SUCCESS"
    assert log.timestamp is not None
