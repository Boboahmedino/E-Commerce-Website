from django.urls import path
from .import views
from django.contrib import admin




admin.site.site_header = "\xa9 Fruitables"
admin.site.site_title = "Fruitables"
admin.site.index_title = f"Fruitables Dashboard"

urlpatterns = [
    path('', views.home, name = 'home'),
    path('shop', views.shop, name = 'shop'),
    path('shop_detail/<int:product_id>/', views.shop_detail, name = 'shop_detail'),
    path('cart', views.cart, name = 'cart'),
    path('checkout', views.checkout, name = 'checkout'),
    path('error', views.error, name = 'error'),
    path('updateitem', views.updateitem, name = 'updateitem'),
    path('processorder', views.processorder, name = 'processorder'),
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('contact', views.contact, name = 'contact'),
    # path('about', views.about, name = 'about'),
] 