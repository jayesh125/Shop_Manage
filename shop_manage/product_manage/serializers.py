from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent_category', 'created_at', 'updated_at']
        read_only_fields = ['user'] 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'SKU', 'quantity', 'category', 'gst_applicable', 'created_at', 'updated_at']
        read_only_fields = ['user'] 