from django.db import models
from django.contrib.auth.models import User

class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    planting_date = models.DateField()
    sunlight = models.CharField(max_length=100)
    watering_frequency = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='plants',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name