"""
URL configuration for quiz_project project.
"""
from django.contrib import admin
from django.urls import path, include

# Admin branding
admin.site.site_header = "Lunovian Technologies Administration"
admin.site.site_title = "Lunovian Technologies Administration"
admin.site.index_title = "Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz_app.urls')),
]

