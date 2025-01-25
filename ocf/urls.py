from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('opencf.html/',views.oc,name='oc'),
    path('calculate/',views.calculate,name='calculate'),
]

