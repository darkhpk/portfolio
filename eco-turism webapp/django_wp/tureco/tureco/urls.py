"""
URL configuration for tureco project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

# Get admin URL from settings (for security)
admin_url = getattr(settings, 'ADMIN_URL', 'admin/')

# Custom error handlers
handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'
handler403 = 'website.views.handler403'

urlpatterns = [
    path('', include('website.urls')),
    path("logs/", include("django_realtime_logs.urls")),
    path(admin_url, admin.site.urls),
    path('accounts/', include('website.urls_auth')),
    path('', RedirectView.as_view(pattern_name='website:search', permanent=False)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)