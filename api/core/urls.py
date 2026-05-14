from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .upload_views import FileUploadView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('leads/', include('leads.urls')),
    path('q/', include('smartqr.public_urls')),
    # Same redirect/PNG handlers under /smartqr/q/ for reverse proxies that only forward /smartqr/*.
    path('smartqr/q/', include('smartqr.public_urls')),
    path('smartqr/', include('smartqr.urls')),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
