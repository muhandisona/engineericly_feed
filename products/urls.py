from django.urls import path
from . import views

urlpatterns = [
    path('api/gallery', views.api_gallery_view, name='api_gallery'),
    path('', views.feed_view, name='feed'),
]
