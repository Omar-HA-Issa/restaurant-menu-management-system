from django.db import connection

def get_menu_items_per_restaurant():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM menu_items_per_restaurant
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_dietary_restrictions_distribution():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM dietary_restrictions_distribution
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_price_analysis():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM price_analysis_per_restaurant
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]