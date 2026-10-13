import requests
from django.conf import settings
from django.shortcuts import render


def weather_home(request):
    city = request.GET.get('city', '')
    weather_data = None

    if city:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            'q': city,
            'appid': settings.OPENWEATHER_API_KEY,
            'units': 'metric'
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            weather_data = response.json()

    return render(request, 'weather/home.html', {
        'city': city,
        'weather': weather_data
    })