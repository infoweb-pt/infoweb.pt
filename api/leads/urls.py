from django.urls import path
from .views import (
    LostCustomerLeadView,
    PresenceScoreLeadView,
    ToolContactLeadView,
    NewLeadsView,
)

urlpatterns = [
    path('lost-customers/', LostCustomerLeadView.as_view(), name='leads-lost-customers'),
    path('presence-score/', PresenceScoreLeadView.as_view(), name='leads-presence-score'),
    path('tool-contact/', ToolContactLeadView.as_view(), name='leads-tool-contact'),
    path('new/', NewLeadsView.as_view(), name='leads-new'),
]
