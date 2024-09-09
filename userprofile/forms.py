from django import forms
from .models import Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['profile_img', 'cover_image', 'major_subject', 'description']
       
