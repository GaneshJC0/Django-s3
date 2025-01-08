from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    # Specify which fields to display in the list view
    list_display = ('id','name', 'description', 'price')  # Add 'name', 'description', and 'price'
    
    # Optionally, you can make the fields searchable and filterable
    search_fields = ('name', 'description')  # Allows searching by name and description
    list_filter = ('price',)  # Allows filtering by price (if applicable)

# Register the Product model with the custom ProductAdmin
admin.site.register(Product, ProductAdmin)