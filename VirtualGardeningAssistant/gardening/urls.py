from django.urls import path
from . import views

urlpatterns = [
    path('', views.gardening_home, name='gardening_home'),
    path('add/', views.add_plant, name='add_plant'),
    path('edit/<int:plant_id>/', views.edit_plant, name='edit_plant'),
    path('delete/<int:plant_id>/', views.delete_plant, name='delete_plant'),
    path('weather/', views.local_weather, name='local_weather'),
    path('identify/', views.identify_plant, name='identify_plant'),
    path('diagnose/',views.diagnose_plant_health,name='diagnose_plant_health'),
]
