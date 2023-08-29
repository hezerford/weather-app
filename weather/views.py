import requests
from django.shortcuts import render, redirect
from .models import City
from googletrans import Translator

def index(request):
    if request.method == 'GET':
        city = request.GET.get('city')
        api = '7c668fe63f7660d8e1fb8dbea1eb6d01'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api}'

        response = requests.get(url).json()
        if response.get('cod') == 200:
            city_data = {
                'city': response['name'],
                'temp': response['main']['temp'],
                'icon': response['weather'][0]['icon'],
            }
            if city_data['city'] != 'None':
                city_obj, created = City.objects.get_or_create(name=city_data['city'])
                if created:
                    city_obj.save()

    cities = City.objects.all()
    city_info = []

    for city in cities:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city.name}&units=metric&appid={api}'
        response = requests.get(url).json()
        if response.get('cod') == 200:
            city_data = {
                'id': city.id,
                'city': response['name'],
                'temp': response['main']['temp'],
                'icon': response['weather'][0]['icon'],
            }
            city_info.append(city_data)

    context = {'city_info': city_info}
    return render(request, 'weather/index.html', context)

def delete_city(request, city_id):
    city = City.objects.get(pk=city_id)
    city.delete()
    return redirect('weather')