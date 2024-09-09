# urls.py
from django.urls import path
from .views import create_teacher_profile,profile,view_teacher_profile,edit_teacher_profile
# from .views import videos



urlpatterns = [
    # path('video/',videos, name='video'),
    path('create_teacher_profile/', create_teacher_profile, name='create_teacher_profile'),
    path('edit_teacher_profile/', edit_teacher_profile, name='edit_teacher_profile'),
    path('', profile, name='profile'),
    path('view_teacher_profile/<int:teacher_id>', view_teacher_profile, name='view_teacher_profile'),


    


]
        # path('view_teacher_profile/<int:user_id>', view_teacher_profile, name='view_teacher_profile'),
