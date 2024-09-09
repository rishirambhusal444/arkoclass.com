# urls.py
from django.urls import path
from .views import create_video,edit_video, edit_subject,video_player,create_video_form
from . import views




urlpatterns = [
    # path('video/',videos, name='video'),



    path('create_video/', create_video, name='create_video'),
    path('create_video_form/', create_video_form, name='create_video_form'), 
    
    path('get_levels/', views.get_levels, name='get_levels'),
    path('get_subjects/', views.get_subjects, name='get_subjects'),

    path('edit_video/<int:video_id>/', edit_video, name='edit_video'),   
    path('edit_subject/<int:subject_id>/', edit_subject, name='edit_subject'),   
    path('video_player/<int:video_id>/', video_player, name='video_player'),




]
    # path('create_class/', create_class, name='create_class'),
