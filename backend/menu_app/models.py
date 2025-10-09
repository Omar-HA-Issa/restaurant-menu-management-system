from django.db import models

class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)  # Add index for searches
    location = models.CharField(max_length=200, db_index=True)  # Add index for location filtering

    def __str__(self):
        return self.name

class Menu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, to_field='restaurant_id')
    version = models.IntegerField(db_index=True)  # Add index for version queries
    date = models.DateField(db_index=True)  # Add index for date filtering

    class Meta:
        indexes = [
            models.Index(fields=['restaurant', 'version'])  # Composite index for restaurant-version queries
        ]

    def __str__(self):
        return f"Menu {self.version} for {self.restaurant.name}"

class MenuSection(models.Model):
    section_id = models.AutoField(primary_key=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, to_field='menu_id')
    section_name = models.CharField(max_length=100, db_index=True)  # Add index for section name searches
    section_order = models.IntegerField(db_index=True)  # Add index for ordering

    def __str__(self):
        return self.section_name

class DietaryRestriction(models.Model):
    restriction_id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=50, unique=True, db_index=True)  # Already indexed due to unique=True

    def __str__(self):
        return self.label

class MenuItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    section = models.ForeignKey(MenuSection, on_delete=models.CASCADE, to_field='section_id')
    name = models.CharField(max_length=100, db_index=True)  # Add index for name searches
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)  # Add index for price filtering
    dietary_restriction = models.ForeignKey(DietaryRestriction, null=True, blank=True,
                                          on_delete=models.SET_NULL, to_field='restriction_id')

    class Meta:
        indexes = [
            models.Index(fields=['section', 'name']),  # Composite index for section-name queries
            models.Index(fields=['price', 'dietary_restriction'])  # Composite index for filtering
        ]

    def __str__(self):
        return self.name

class ProcessingLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, to_field='menu_id')
    status = models.CharField(max_length=50, db_index=True)  # Add index for status filtering
    error_message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)  # Add index for timestamp queries

    class Meta:
        indexes = [
            models.Index(fields=['menu', 'status'])  # Composite index for menu-status queries
        ]

    def __str__(self):
        return f"Log for Menu {self.menu.menu_id}"