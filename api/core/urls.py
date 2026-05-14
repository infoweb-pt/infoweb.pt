from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve as serve_static

from .upload_views import FileUploadView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('leads/', include('leads.urls')),
    path('q/', include('smartqr.public_urls')),
    # Same redirect/PNG handlers under /smartqr/q/ for reverse proxies that only forward /smartqr/*.
    path('smartqr/q/', include('smartqr.public_urls')),
    path('smartqr/', include('smartqr.urls')),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    # Serve user uploads (menu PDFs/images) in all environments.
    # In production this should be fronted by a CDN / reverse proxy for caching.
    re_path(
        r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
        serve_static,
        {'document_root': settings.MEDIA_ROOT},
        name='media',
    ),
]
