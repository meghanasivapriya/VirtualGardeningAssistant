from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PlantForm, PlantHealthDiagnosisForm
from .models import Plant
import requests
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import PlantIdentificationForm

@login_required
def gardening_home(request):
    plants = Plant.objects.filter(owner=request.user)
    return render(
        request,
        'gardening/home.html',
        {'plants': plants}
    )

def add_plant(request):
    if request.method == 'POST':
        form = PlantForm(request.POST)

        if form.is_valid():
            plant = form.save(commit=False)
            plant.owner = request.user
            plant.save()
            messages.success(request, 'Plant added successfully! 🌱')
            return redirect('gardening_home')
    else:
        form = PlantForm()

    return render(request, 'gardening/add_plant.html', {
        'form': form
    })


def edit_plant(request, plant_id):
    plant = get_object_or_404(
        Plant,
        id=plant_id,
        owner=request.user
    )

    if request.method == 'POST':
        form = PlantForm(request.POST, instance=plant)

        if form.is_valid():
            form.save()
            messages.success(request, 'Plant updated successfully! 🌱')
            return redirect('gardening_home')
    else:
        form = PlantForm(instance=plant)

    return render(request, 'gardening/edit_plant.html', {
        'form': form,
        'plant': plant
    })


def delete_plant(request, plant_id):
    plant = get_object_or_404(
        Plant,
        id=plant_id,
        owner=request.user
    )

    if request.method == 'POST':
        plant.delete()
        messages.success(request, 'Plant deleted successfully.')
        return redirect('gardening_home')

    return render(request, 'gardening/delete_plant.html', {
        'plant': plant
    })


def local_weather(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return JsonResponse(
            {'error': 'Location coordinates are missing.'},
            status=400
        )

    try:
        response = requests.get(
            'https://api.openweathermap.org/data/2.5/weather',
            params={
                'lat': lat,
                'lon': lon,
                'appid': settings.OPENWEATHER_API_KEY,
                'units': 'metric',
            },
            timeout=10,
        )

        if response.status_code != 200:
            return JsonResponse(
                {'error': 'Unable to retrieve weather. Please try again later.'},
                status=502
            )

        data = response.json()

        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        condition = data['weather'][0]['description']

        plants = Plant.objects.filter(owner=request.user)

        recommendations = plant_care_recommendations(
            temperature,
            humidity,
            condition,
            plants
        )

        return JsonResponse({
            'temperature': temperature,
            'humidity': humidity,
            'condition': condition,
            'recommendations': recommendations,
        })

    except (requests.RequestException, ValueError, KeyError):
        return JsonResponse(
            {'error': 'Unable to retrieve weather right now.'},
            status=502
        )


def plant_care_recommendations(temperature, humidity, condition, plants):
    recommendations = []
    condition = condition.lower()

    for plant in plants:
        tips = []

        # Temperature guidance
        if temperature >= 38:
            tips.append(
                "Extreme heat: move container plants away from harsh "
                "afternoon sun if they show heat stress. Check soil moisture "
                "and avoid watering automatically if the soil is already wet."
            )
        elif temperature >= 35:
            tips.append(
                "Very hot weather: check soil moisture daily, especially "
                "for plants in pots. Water only when the soil or plant's "
                "care requirements indicate it is needed."
            )
        elif temperature >= 30:
            tips.append(
                "Warm weather: monitor soil moisture more frequently. "
                "Containers and small pots may dry out faster."
            )
        elif temperature <= 5:
            tips.append(
                "Very cold conditions: protect cold-sensitive plants from "
                "cold exposure and check their species-specific temperature needs."
            )
        elif temperature <= 10:
            tips.append(
                "Cool weather: check soil before watering because plants "
                "may use water more slowly in cooler conditions."
            )

        # Humidity guidance
        if humidity >= 85:
            tips.append(
                "Very high humidity: improve airflow around the plant, "
                "avoid unnecessarily wetting foliage, and watch for "
                "spreading spots or fungal growth."
            )
        elif humidity <= 30:
            tips.append(
                "Low humidity: monitor for leaf curling or dry edges. "
                "Check soil moisture before watering; low air humidity "
                "does not necessarily mean the soil is dry."
            )

        # Weather condition guidance
        if "rain" in condition or "drizzle" in condition:
            tips.append(
                "Rain or drizzle: check the soil and pot drainage before "
                "watering. Rainfall may not reach plants sheltered under cover."
            )

        if "thunderstorm" in condition:
            tips.append(
                "Thunderstorms: move vulnerable potted plants to a sheltered "
                "spot if practical, and secure them against strong winds."
            )

        if "clear" in condition:
            tips.append(
                "Clear skies: check whether the plant's current light exposure "
                "matches its sunlight requirement. Avoid sudden changes to "
                "direct sunlight."
            )

        if "snow" in condition or "sleet" in condition:
            tips.append(
                "Frozen precipitation: protect sensitive plants from freezing "
                "conditions and check the plant's cold tolerance."
            )

        if not tips:
            tips.append(
                "No special action is indicated by these weather readings. "
                "Check the soil moisture, drainage, and the plant's usual care needs."
            )

        recommendations.append({
            "plant_id": plant.id,
            "plant": plant.name,
            "tips": tips,
        })

    return recommendations


@login_required
def identify_plant(request):
    results = []
    error = None

    if request.method == 'POST':
        form = PlantIdentificationForm(request.POST, request.FILES)

        if form.is_valid():
            if not settings.PLANTNET_API_KEY:
                error = "Plant identification API key is not configured."
            else:
                image = form.cleaned_data['image']

                try:
                    response = requests.post(
                        'https://my-api.plantnet.org/v2/identify/all',
                        params={
                            'api-key': settings.PLANTNET_API_KEY
                        },
                        files={
                            'images': (
                                image.name,
                                image,
                                image.content_type
                            )
                        },
                        data={'organs': 'auto'},
                        timeout=30,
                    )

                    if response.status_code == 200:
                        data = response.json()

                        for item in data.get('results', [])[:5]:
                            species = item.get('species', {})

                            results.append({
                                'name': species.get(
                                    'scientificNameWithoutAuthor',
                                    'Unknown species'
                                ),
                                'common_names': species.get(
                                    'commonNames', []
                                ),
                                'confidence': round(
                                    item.get('score', 0) * 100, 2
                                ),
                            })

                        if not results:
                            error = (
                                "No likely plant species found. "
                                "Try a clearer photo."
                            )
                    else:
                        error = (
                            "Plant identification failed. "
                            "Please try again."
                        )

                except (requests.RequestException, ValueError):
                    error = (
                        "Unable to contact the plant identification "
                        "service. Please try again later."
                    )
    else:
        form = PlantIdentificationForm()

    return render(
        request,
        'gardening/identify_plant.html',
        {
            'form': form,
            'results': results,
            'error': error,
        }
    )


@login_required
def diagnose_plant_health(request):
    results = None
    error = None

    if request.method == 'POST':
        form = PlantHealthDiagnosisForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            if not settings.PLANTHEALTHENGINE_API_KEY:
                error = "Plant health API key is not configured."
            else:
                image = form.cleaned_data['image']
                crop = form.cleaned_data['crop']

                try:
                    response = requests.post(
                        'https://planthealthengine.com/api/v1/diagnose',
                        headers={
                            'Authorization': (
                                f'Bearer {settings.PLANTHEALTHENGINE_API_KEY}'
                            )
                        },
                        files={
                            'image': (
                                image.name,
                                image,
                                image.content_type
                            )
                        },
                        data={'crop': crop},
                        timeout=30,
                    )

                    if response.status_code == 200:
                        data = response.json()
                        treatment = data.get('treatment') or {}

                        results = {
                            'crop': crop.title(),
                            'status': data.get('result', 'uncertain'),
                            'disease': (
                                (data.get('disease') or '')
                                .replace('_', ' ')
                                .title()
                            ),
                            'confidence': round(
                                float(data.get('confidence') or 0) * 100,
                                2
                            ),
                            'low_confidence': data.get(
                                'confidence_below_threshold', True
                            ),
                            'cure': treatment.get('cure', ''),
                            'prevention': treatment.get(
                                'prevention', ''
                            ),
                            'sprays': treatment.get(
                                'recommended_sprays', []
                            ),
                        }

                    elif response.status_code == 401:
                        error = "API key rejected. Check your key."

                    elif response.status_code == 422:
                        error = (
                            "The photo could not be analysed. "
                            "Upload a clearer, well-lit leaf photo."
                        )

                    elif response.status_code == 429:
                        error = (
                            "API limit reached. Check your monthly "
                            "quota or try again later."
                        )

                    else:
                        error = (
                            "Diagnosis service error. "
                            "Please try again later."
                        )

                except (requests.RequestException, ValueError):
                    error = (
                        "Could not complete the diagnosis. "
                        "Check your connection and try again."
                    )
    else:
        form = PlantHealthDiagnosisForm()

    return render(
        request,
        'gardening/diagnose_plant_health.html',
        {
            'form': form,
            'results': results,
            'error': error,
        }
    )