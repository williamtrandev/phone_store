from django.urls import path, re_path
from applications.website.views import auth_view, product_view, checkout_view

urlpatterns = [
    # Authentication
    path('', auth_view.index, name='index'),
    path('login', auth_view.user_login, name="login"),
    path('register', auth_view.user_register, name="register"),
    path('logout', auth_view.user_logout, name="logout"),

    # Product
    path('phones', product_view.product_page, name="phone_list"),
    path('phones/<str:phone_id>', product_view.product_detail, name="phone_detail"),
    path('accessories', product_view.product_page, name="accessory_list"),
    path('accessories/<str:accessory_id>', product_view.accessory_detail, name="accessory_detail"),
    path('api/phones/page/<int:page>', product_view.api_list_product_paging, name="api_list_phone_paging"),
    path('api/accessories/page/<int:page>', product_view.api_list_product_paging, name="api_list_accessory_paging"),

    # Cart
    path('api/cart', checkout_view.add_product_to_cart, name="add_product_to_cart"),
    path('api/cart/<str:cart_id>', checkout_view.action_product_in_cart, name="action_product_in_cart"),
    path('cart', checkout_view.cart_page, name="cart_page"),

    # Order
    path('api/order', checkout_view.checkout, name="checkout"),
    path('order', checkout_view.order_page, name="order_page"),
]
