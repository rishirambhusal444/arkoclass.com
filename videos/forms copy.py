from django import forms
from .models import Faculty, Level, Subject, Video

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['faculty_name']

class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = ['level_name']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['chapter_number', 'video_name', 'video', 'description']
