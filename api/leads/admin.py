from django.contrib import admin
from .models import LostCustomerLead, PresenceScoreLead, ToolContactLead


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
