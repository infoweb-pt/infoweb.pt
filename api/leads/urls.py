from django.urls import path
from .views import LostCustomerLeadView, PresenceScoreLeadView

urlpatterns = [
    path('lost-customers/', LostCustomerLeadView.as_view(), name='leads-lost-customers'),
    path('presence-score/', PresenceScoreLeadView.as_view(), name='leads-presence-score'),
]
