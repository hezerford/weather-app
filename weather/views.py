import requests
from django.views.generic import ListView, DeleteView, View, FormView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import City
from googletrans import Translator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class CustomLoginView(LoginView):
    template_name = 'weather/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('weather')

class RegisterPage(FormView):
    template_name = 'weather/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('weather')
        return super(RegisterPage, self).get(*args, **kwargs)
        
class CityListView(LoginRequiredMixin, ListView):
    model = City
    template_name = 'weather/main.html'
    context_object_name = 'city_info'
    login_url = '/login/'

    def get_queryset(self):
        return City.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api_key = '7c668fe63f7660d8e1fb8dbea1eb6d01' # your api
        city_info = []
        translator = Translator()

        for city in self.object_list: # Используйте self.object_list для доступа к городам из базы данных
            temperature_unit = city.temperature_unit
            units = 'metric'
            
            if temperature_unit == 'F':
                units = 'imperial'
            elif temperature_unit == 'K':
                units = 'standard'

            url = f'https://api.openweathermap.org/data/2.5/weather?q={city.name}&units={units}&appid={api_key}'
            response = requests.get(url).json()
            if response.get('cod') == 200:
                city_name_en = response['name']
                city_name_ru = translator.translate(city_name_en, src='en', dest='ru').text

                city_data = {
                    'id': city.id,
                    'city': city_name_ru,
                    'temp': response['main']['temp'],
                    'temp_unit': temperature_unit,
                    'icon': response['weather'][0]['icon'],
                }
                city_info.append(city_data)

        context['city_info'] = city_info
        return context
    
    def post(self, request, *args, **kwargs):
        city_name = request.POST.get('city')
        if city_name:
            new_city = City.objects.create(user=request.user, name=city_name, temperature_unit=request.POST.get('temperature_unit', 'C'))
        return redirect('weather')

class CityDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        city = City.objects.get(pk=pk)
        if city.user == request.user:
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