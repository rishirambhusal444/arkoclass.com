# urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('create_article/', views.create_article, name='create_article'),
    path('article_home/', views.article_home, name='article_home'),
    path('article_view/<int:id>/', views.article_view, name='article_view'),
    
    path('upload_image/', views.upload_image, name='upload_image'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
