FROM python:3

ENV DJANGO_SETTINGS_MODULE=WeatherApp.settings

WORKDIR /weather

COPY requirements.txt /weather/

RUN pip install -r requirements.txt

COPY . /weather/

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]