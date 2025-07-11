"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from myapp import views

urlpatterns = [
    path('', include('myapp.urls')),
    path("", views.indexpage),
    path("register", views.userregister),
    path("login", views.userlogin, name="login"),
    path("fetchregisterdata", views.fetchregisterdata),
    path("fetchlogindata", views.fetchlogindata),
    path("logout", views.logout),
    path("shop", views.showproductpage, name="shop_home"),
    path("shop/category/<int:category_id>/", views.showproductpage, name="category_products"),
    path("single-product/<int:id>/", views.singleproductpage, name="single_product"),
    path("cart", views.showcart, name="showcart"),
    path("insertintocart", views.insertintocart),
    path("updatecart/<int:item_id>/<str:action>/", views.update_cart_quantity, name="updatecart"),
    path("deletefromcart/<int:cart_id>/", views.deletefromcart, name="deletefromcart"),
    path("contact-us", views.contactuspage),
    path("fetchcontactusdata", views.fetchcontactusdata),
    path("customization", views.customizationpage),
    path("yourorders", views.yourorders),
    path("yourcustomization", views.yourcustomization),
    path("fetchcustomizedata", views.fetchcustomizedata),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("rent/<int:product_id>/", views.rent_product, name="rent_product"),
    path("fetchrentaldata", views.fetch_rental_data, name="fetch_rental_data"),
    path('checkout',views.checkout,name='checkout'),
    path('create-order', views.create_order, name='create_order'),
    path("update-payment-status", views.update_payment_status, name="update_payment_status"),
    path("update-task-status/<int:task_id>/", views.update_task_status, name="update_task_status"),
    path("rent-history", views.rent_history, name="rent_history"),

   ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)