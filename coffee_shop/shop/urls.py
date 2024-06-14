from django.urls import path
from . import views
from .views import update_cart_item, delete_cart_item, cart_total

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cart/update_item/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('cart/delete_item/<int:item_id>/', delete_cart_item, name='delete_cart_item'),
    path('cart/total/', cart_total, name='cart_total'),
]
