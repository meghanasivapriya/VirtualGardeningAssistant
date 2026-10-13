from django import forms
from .models import Plant

class PlantIdentificationForm(forms.Form):
    image = forms.ImageField(
        label="Upload a plant photo",
        help_text="Upload a clear JPG or PNG image of one plant."
    )

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            'name',
            'species',
            'planting_date',
            'sunlight',
            'watering_frequency',
            'notes',
        ]

        widgets = {
            'planting_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

class PlantHealthDiagnosisForm(forms.Form):
    CROP_CHOICES = [
        ('tomato', 'Tomato'),
        ('potato', 'Potato'),
    ]

    image = forms.ImageField(
        label="Upload an affected plant photo"
    )

    crop = forms.ChoiceField(
        choices=CROP_CHOICES,
        label="Select crop"
    )