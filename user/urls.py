from django.urls import path
from .import views
from django.contrib import admin
urlpatterns=[
    path('user/',views.cms,name='cms'),
    path('accounts/',views.accountsettings,name='account'),
    
]

    
