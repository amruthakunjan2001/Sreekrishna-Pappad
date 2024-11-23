"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('user',views.user,name='user'),
    path('my-orders/<int:order_id>/', views.order_details_view, name='userorder'),  
    path('cart',views.cart,name='cart'),
    path('login/',views.login_view, name='login'),  # Example login view

    path('checkout',views.checkout,name='checkout'),
    path('contact',views.contact,name='contact'),
    path('shop_detail/<int:product_id>/', views.detail, name='shop_detail'),
    path('shop',views.display,name='shop'),
    path('shop/<int:product_id>/', views.detail, name='shop'),
    

    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/', views.cart_detail, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('payment_success/', views.razorpay_success, name='payment_success'),
    path('product/<int:product_id>/', views.detail, name='shop_detail'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('blank',views.admin,name='blank'),
    path('logout',views.logout,name='logout'),
    path('product_list',views.product_list,name='product_list'),
    path('users/',views.user_management,name='user_management'),
    path('edit_user/<int:pk>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
    path('product_management/', views.product_management, name='product_management'),
    path('category/<category>/', views.category_products_view, name='category_products'),

    path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('order_management/', views.order_management, name='order_management'),
    path('order/<int:order_id>/', views.order_details, name='order_details'),  
    path('order/delete/<int:pk>/', views.delete_order, name='delete_order'),
    path('delivery-boys/', views.delivery_boy_management, name='delivery_boy_management'),
    path('delivery-boy/update/<int:delivery_boy_id>/', views.update_delivery_boy, name='update_delivery_boy'),
    path('delivery-boy/delete/<int:delivery_boy_id>/', views.delete_delivery_boy, name='delete_delivery_boy'),
    path('delivery-boy/<int:delivery_boy_id>/orders/', views.view_delivery_boy_orders, name='view_delivery_boy_orders'),
    path('delivery-boy/details/<int:delivery_boy_id>/', views.view_delivery_boy_details, name='view_delivery_boy_details'),
    path('delivery-boy/dashboard/', views.delivery_boy_dashboard, name='delivery_boy_dashboard'),
    path('delivery-boy/update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),


    path('forgot',views.forgot_password,name="forgot"),
    path('reset/<token>',views.reset_password,name='reset_password'),
    path('add/',views.add_product, name='product_create'),
    # path('shop/',include('shop.urls')),




    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)