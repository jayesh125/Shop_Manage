from django.contrib import admin
from .models import Product, Category

# Register your models here.

@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "price", "SKU", "quantity", "category", "user", "gst_applicable", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["name", "description", "SKU"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["name", "description"]
    ordering = ["name"]

    