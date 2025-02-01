from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('pipe_calculation/',views.pipe_calculation,name='pipe_calculation'),
]