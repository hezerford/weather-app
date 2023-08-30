import requests
from django.views.generic import ListView, DeleteView, View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import City
from googletrans import Translator

class CityListView(ListView):
    model = City
    template_name = 'weather/index.html'
    context_object_name = 'city_info'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api_key = '7c668fe63f7660d8e1fb8dbea1eb6d01' # your api
        city_info = []
        translator = Translator()

        for city in context['city_info']:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city.name}&units=metric&appid={api_key}'
            response = requests.get(url).json()
            if response.get('cod') == 200:
                city_name_en = response['name']
                city_name_ru = translator.translate(city_name_en, src='en', dest='ru').text

                city_data = {
                    'id': city.id,
                    'city': city_name_ru,
                    'temp': response['main']['temp'],
                    'icon': response['weather'][0]['icon'],
                }
                city_info.append(city_data)

        context['city_info'] = city_info
        return context
    
    def post(self, request, *args, **kwargs):
        city_name = request.POST.get('city')
        if city_name:
            City.objects.create(name=city_name)
        return redirect('weather')


class CityDeleteView(View):

    def post(self, request, pk, *args, **kwargs):
        city = City.objects.get(pk=pk)
        city.delete()
        return redirect('weather')
'''
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
'''