# forms.py

from django import forms
from .models import Slider

class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['image', 'title', 'description']
