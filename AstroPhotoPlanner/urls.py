
from django.contrib import admin
from django.urls import include, path
from AstroPhotoPlanner import views

urlpatterns = [
    path('', views.index_page),
]
