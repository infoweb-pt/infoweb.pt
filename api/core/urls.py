from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('leads/', include('leads.urls')),
    path('q/', include('smartqr.public_urls')),
    path('smartqr/', include('smartqr.urls')),
]
