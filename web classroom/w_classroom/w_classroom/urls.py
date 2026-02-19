"""
URL configuration for web_classroom project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('classroom.urls')),
]
