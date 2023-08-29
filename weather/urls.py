from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='weather'),
    path('delete/<int:city_id>/', views.delete_city, name='delete_city'),
]