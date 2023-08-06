"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from . import views
from . import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fourohfour/', views.fourohfour),

    # user pages
    path('', views.home),
    path('login/', views.login, name="login"),
    path('register/', views.register),
    path('logout/', api.logout),

    # product pages
    path('products/', views.products_page),
    path('errors/', views.errors_page),
    path('products/?page=<int:num>', views.products_page),
    path('products/analytics', views.products_analytics),
    path('product/<str:name>/', views.product_view),
    path('product/<str:name>/analytics/', views.product_analytics),

    ### api ###
    path('api/create/product', api.create_product),
    path('api/edit/product/<str:name>', api.edit_product),
    path('api/delete/product/<str:name>', api.delete_product),
    path('api/create/dependency/<str:prod_name>', api.create_dependency),
    path('api/edit/dependency/<str:prod_name>', api.edit_dependency),
    path('api/delete/dependency/', api.delete_dependency),
    path('api/edit/commit-history/<str:name>', api.commit_history_request),
    path('api/edit/commit-history/', api.commit_history_request)
]
