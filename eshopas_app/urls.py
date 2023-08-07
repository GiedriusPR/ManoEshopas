from django.urls import path, include
from . import views
from PIL import Image


urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/add_comment/', views.product_detail, name='add_comment'),
    path('category/', views.category, name='category_list'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart-detail/', views.cart_detail, name='cart_detail'),
    path('cart-count/', views.cart_count, name='cart_count'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('billing_address/', views.billing_address, name='billing_address'),
    path('stripe_payment/', views.stripe_payment, name='stripe_payment'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-favorites/', views.my_favorites_view, name='my_favorites'),
    path('toggle-favorite/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('order_detail/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('order_list/', views.order_list, name='order_list'),
    path('update_quantity/<int:product_id>/', views.update_quantity, name='update_quantity'),
    path('remove_item/<int:product_id>/', views.remove_item, name='remove_item'),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
]
