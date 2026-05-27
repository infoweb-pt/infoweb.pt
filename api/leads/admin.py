from django.contrib import admin
from .models import (
    CompetitorVisibilityGapLead,
    LostCustomerLead,
    PresenceScoreLead,
    ToolContactLead,
    WebsiteHealthScorecardLead,
)


@admin.register(LostCustomerLead)
class LostCustomerLeadAdmin(admin.ModelAdmin):
    list_display = ('email', 'weekly_loss', 'monthly_loss', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('email',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(PresenceScoreLead)
class PresenceScoreLeadAdmin(admin.ModelAdmin):
    list_display = ('email', 'score', 'created_at')
    list_filter = ('created_at', 'score')
    search_fields = ('email',)
    readonly_fields = ('answers', 'created_at')
    ordering = ('-created_at',)


@admin.register(ToolContactLead)
class ToolContactLeadAdmin(admin.ModelAdmin):
    list_display = ('email', 'source', 'created_at')
    list_filter = ('created_at', 'source')
    search_fields = ('email',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(WebsiteHealthScorecardLead)
class WebsiteHealthScorecardLeadAdmin(admin.ModelAdmin):
    list_display = ('email', 'url', 'score', 'created_at')
    list_filter = ('created_at', 'score')
    search_fields = ('email', 'url')
    readonly_fields = ('checks', 'fixes', 'created_at')
    ordering = ('-created_at',)


@admin.register(CompetitorVisibilityGapLead)
class CompetitorVisibilityGapLeadAdmin(admin.ModelAdmin):
    list_display = ('email', 'score', 'created_at')
    list_filter = ('created_at', 'score')
    search_fields = ('email',)
    readonly_fields = ('answers', 'created_at')
    ordering = ('-created_at',)
