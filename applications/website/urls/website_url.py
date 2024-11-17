from django.urls import path, re_path
from applications.website.views import website_view

urlpatterns = [
    path('', website_view.index, name='index'),
    path('login', website_view.user_login, name="login"),
    path('register', website_view.user_register, name="register"),
    path('logout', website_view.user_logout, name="logout")
]
