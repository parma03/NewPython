"""
Root URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1 Routes
    path('api/v1/auth/', include('presentation.api.auth.urls')),
    path('api/v1/users/', include('presentation.api.users.urls')),
    path('api/v1/products/', include('presentation.api.products.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
