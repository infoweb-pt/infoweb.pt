from django.urls import re_path

from .public_views import QRCodePngView, RedirectView

urlpatterns = [
    re_path(r'^(?P<slug>[A-Za-z0-9]{4,12})\.png$', QRCodePngView.as_view(), name='smartqr-png'),
    re_path(r'^(?P<slug>[A-Za-z0-9]{4,12})$', RedirectView.as_view(), name='smartqr-redirect'),
]
