from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Creates database views'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            with open('menu_app/sql/views.sql', 'r') as file:
                sql = file.read()
                cursor.execute(sql)