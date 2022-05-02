from django.urls import path
from .import views
from django.contrib import admin

urlpatterns =[
    path('',views.dashboard,name='dashboard'),
    path('customer/<int:pk_id>/',views.customer,name='customer'),
    path('products/',views.product,name='product'),
    path('order_form/<int:pk>/',views.orderform,name='orderform'),
    path('updates/<int:pk>/',views.updates,name='updates'),
    path('delete/<int:pk>/',views.deleteOrder,name='delete'),

]