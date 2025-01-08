# views.py

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Product , Profile  ,  Cart , CartItem
from .serializers import UserSerializer, ProductSerializer, ProductCreateSerializer, ProfileUpdateSerializer , CartSerializer, CartItemSerializer


# User Registration
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Optionally, create an empty profile for the user
            Profile.objects.create(user=user)
            return Response({"message": "User created successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login (JWT Token)
class LoginView(TokenObtainPairView):
    pass  # We can use the built-in JWT login view


# Product Listing (All Users)
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# Add Product (Admin Only)
@api_view(['POST'])
@permission_classes([IsAdminUser])  # Only admins can add products
def add_product(request):
    if request.method == 'POST':
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View Profile (Authenticated Users)
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Only authenticated users can access their profile
def view_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProfileUpdateSerializer(profile)
    return Response(serializer.data)


# Update Profile (Authenticated Users)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # Only authenticated users can update their profile
def update_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

   

    # Partial update - allows the user to update specific fields
    serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# Helper function to get or create a user's cart
def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

# View Cart (Authenticated Users)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    cart = get_or_create_cart(request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

# Add Product to Cart (Authenticated Users)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)  # Default to 1 if no quantity provided

    # Check if product exists
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    # Get or create the user's cart
    cart = get_or_create_cart(request.user)

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # If the product is already in the cart, update the quantity
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    return Response({"message": "Product added to cart", "cart": CartSerializer(cart).data}, status=status.HTTP_200_OK)

# Remove Product from Cart (Authenticated Users)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    product_id = request.data.get('product_id')

    # Check if product exists
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    # Get or create the user's cart
    cart = get_or_create_cart(request.user)

    # Try to get the cart item to remove
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        return Response({"message": "Product removed from cart"}, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response({"error": "Product not in cart"}, status=status.HTTP_404_NOT_FOUND)
