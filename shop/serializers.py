from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Product, Review, Profile

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', "manufacturer","release_year", 'description', 'price', 'stock', 'available', 'created', 'updated']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    favorite_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user','favorite_products']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class ProductFilterSerializer(serializers.Serializer):
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    manufacturers = serializers.ListField(child=serializers.CharField(), required=False)
    min_year = serializers.IntegerField(required=False)
    max_year = serializers.IntegerField(required=False)

class ReviewSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'profile', 'rating', 'comment', 'created', 'updated']
        read_only_fields = ['created', 'updated']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance