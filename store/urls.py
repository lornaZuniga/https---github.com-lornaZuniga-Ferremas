from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='store_home'),
    path('carrito/', views.cart, name='store_cart'),
]

