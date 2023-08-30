from django.urls import path
from .views import CityListView, CityDeleteView

urlpatterns = [
    path('', CityListView.as_view(), name='weather'),  # Пустой путь для списка городов
    path('delete/<int:pk>/', CityDeleteView.as_view(), name='delete_city'),
]