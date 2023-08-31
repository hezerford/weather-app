from django.urls import path
from .views import CityListView, CityDeleteView, CustomLoginView, RegisterPage, LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', CityListView.as_view(), name='weather'),  # Пустой путь для списка городов
    path('delete/<int:pk>/', CityDeleteView.as_view(), name='delete_city'),
]