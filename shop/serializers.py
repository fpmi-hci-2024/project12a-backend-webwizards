from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', "manufacturer","release_year", 'description', 'price', 'stock', 'available', 'created', 'updated']

class ProductFilterSerializer(serializers.Serializer):
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    manufacturers = serializers.ListField(child=serializers.CharField(), required=False)
    min_year = serializers.IntegerField(required=False)
    max_year = serializers.IntegerField(required=False)