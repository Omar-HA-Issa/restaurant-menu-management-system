import json
import pytest
from django.urls import reverse

# factories now live in backend/tests/
from tests.factories import make_menu, make_section, make_item

@pytest.mark.django_db
def test_get_restaurant_list(client):
    url = reverse("restaurant-list")
    resp = client.get(url)
    assert resp.status_code == 200

@pytest.mark.django_db
def test_get_menu_list(client):
    make_menu()
    make_menu()
    url = reverse("menu-list")
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 2

@pytest.mark.django_db
def test_create_menu_item(client):
    s = make_section()
    url = reverse("menuitem-list")
    payload = {
        "section": s.pk,
        "name": "Water",
        "description": "Still",
        "price": "1.00",
    }
    resp = client.post(url, data=json.dumps(payload), content_type="application/json")
    assert resp.status_code in (200, 201)
    body = resp.json()
    assert body.get("name") == "Water"

@pytest.mark.django_db
def test_get_menu_items(client):
    s = make_section()
    make_item(section=s, name="Soup")
    make_item(section=s, name="Salad")
    url = reverse("menuitem-list")
    resp = client.get(url)
    assert resp.status_code == 200
    names = {row["name"] for row in resp.json()}
    assert {"Soup", "Salad"}.issubset(names)

# --- ADDITIONAL TEST BELOW ---

@pytest.mark.django_db
def test_created_item_appears_in_list(client):
    s = make_section()
    url = reverse("menuitem-list")
    client.post(
        url,
        data=json.dumps({"section": s.pk, "name": "Tea", "description": "Hot", "price": "2.00"}),
        content_type="application/json",
    )
    resp = client.get(url)
    assert resp.status_code == 200
    names = {row["name"] for row in resp.json()}
    assert "Tea" in names
