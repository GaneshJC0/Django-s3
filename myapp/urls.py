from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),  # Admin only

    path('profile/', views.view_profile, name='view_profile'),  # GET request to view profile
    path('profile/update/', views.update_profile, name='update_profile'),  # PUT request to update profile


    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),

    

]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)