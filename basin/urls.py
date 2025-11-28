from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.page,name='page'),
     path('water/predict/', views.water_predict, name='water_predict')
    ]