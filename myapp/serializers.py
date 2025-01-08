# serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Product , Cart, CartItem


# Profile Serializer to handle additional fields for the user
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'mobile_number', 'address']  # Profile fields, image is optional


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'mobile_number', 'address'] 

# User Serializer to handle user registration (no profile included)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']  # Only basic fields (username, email, password)

    def create(self, validated_data):
        # Create the user instance (without profile data for now)
        user = User.objects.create_user(**validated_data)
        return user


# Product Serializer to view product details
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price',  'image']


# Product Create Serializer to add new products
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price',  'image']





# CartItem serializer (for displaying cart items)
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Include product details in the cart item

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

# Cart serializer (for displaying the entire cart)
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)  # List of cart items

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']
