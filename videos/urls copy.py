# urls.py
from django.urls import path
from .views import create_video
# from .views import videos

from .views import create_class
from .views import get_levels,get_subjects




urlpatterns = [
    # path('video/',videos, name='video'),



    path('create_video/', create_video, name='create_video'),
    path('create_class/', create_class, name='create_class'),
    path('create_class/get_levels/', get_levels, name='get_levels'),
    path('create_class/get_subjects/', get_subjects, name='get_subjects'),


]
