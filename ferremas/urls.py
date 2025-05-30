from django.contrib import admin
from django.urls import path, include
from frontend import views as frontend_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', frontend_views.login_view, name='login'),
    path('logout/', frontend_views.logout_view, name='logout'),
    path('api/', include('products.urls')),  #  rutas API products
    path('', frontend_views.index, name='index'),
    path('store/', include('store.urls')),  # nueva tienda
]


