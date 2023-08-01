from django.urls import path, include
from . import views
from .views import CategoryListView
from .views import cart_detail


urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart-detail/', cart_detail, name='cart_detail'),
    path('cart-count/', views.cart_count, name='cart_count'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
]
