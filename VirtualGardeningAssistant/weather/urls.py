from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_home, name = 'weather_home'),

]