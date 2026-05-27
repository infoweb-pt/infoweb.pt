from django.urls import path
from .views import (
    CompetitorVisibilityGapLeadView,
    LostCustomerLeadView,
    PresenceScoreLeadView,
    ToolContactLeadView,
    WebsiteHealthScorecardLeadView,
    NewLeadsView,
)

urlpatterns = [
    path('lost-customers/', LostCustomerLeadView.as_view(), name='leads-lost-customers'),
    path('presence-score/', PresenceScoreLeadView.as_view(), name='leads-presence-score'),
    path('tool-contact/', ToolContactLeadView.as_view(), name='leads-tool-contact'),
    path(
        'website-health-scorecard/',
        WebsiteHealthScorecardLeadView.as_view(),
        name='leads-website-health-scorecard',
    ),
    path(
        'competitor-visibility-gap/',
        CompetitorVisibilityGapLeadView.as_view(),
        name='leads-competitor-visibility-gap',
    ),
    path('new/', NewLeadsView.as_view(), name='leads-new'),
]
