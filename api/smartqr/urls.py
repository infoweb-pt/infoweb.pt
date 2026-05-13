from django.urls import path

from .views import (
    SmartQRCodeClaimView,
    SmartQRCodeDetailView,
    SmartQRCodeListCreateView,
    SmartQRCodeScansView,
    SmartQRCodeStatsView,
)

urlpatterns = [
    path('codes/', SmartQRCodeListCreateView.as_view(), name='smartqr-codes-create'),
    path('codes/<slug:slug>/', SmartQRCodeDetailView.as_view(), name='smartqr-codes-detail'),
    path('codes/<slug:slug>/scans/', SmartQRCodeScansView.as_view(), name='smartqr-codes-scans'),
    path('codes/<slug:slug>/stats/', SmartQRCodeStatsView.as_view(), name='smartqr-codes-stats'),
    path('codes/<slug:slug>/claim/', SmartQRCodeClaimView.as_view(), name='smartqr-codes-claim'),
]
