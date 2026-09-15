from django.forms import ModelForm
from . import models

class PostAlgorithm(ModelForm):
    class Meta:
        model = models.Algorithm
        fields = ["name", "category", "moves", "description"]