# urls.py
from django.urls import path
from .views import home,create_slider,slider_created
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    # path('video/',videos, name='video'),



    path('', home, name='home'),
    path('slider_create/', create_slider, name='create_slider'),
    path('slider_view/', slider_created, name='slider_created'),    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
