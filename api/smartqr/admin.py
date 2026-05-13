from django.contrib import admin
from django.db.models import Count

from .models import SmartQRCode, SmartQRScan


class SmartQRScanInline(admin.TabularInline):
    model = SmartQRScan
    extra = 0
    can_delete = False
    max_num = 100
    fields = (
        'created_at',
        'country',
        'device_type',
        'os_family',
        'browser_family',
        'referrer',
        'is_bot',
    )
    readonly_fields = fields
    ordering = ('-created_at',)

    def has_add_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')


@admin.register(SmartQRCode)
class SmartQRCodeAdmin(admin.ModelAdmin):
    list_display = (
        'slug',
        'tool_source',
        'label',
        'owner_user',
        'is_active',
        'scan_total',
        'created_at',
    )
    search_fields = ('slug', 'label', 'owner_email')
    list_filter = ('tool_source', 'is_active', 'created_at')
    inlines = [SmartQRScanInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_scan_total=Count('scans'))

    @admin.display(ordering='_scan_total')
    def scan_total(self, obj):
        return getattr(obj, '_scan_total', 0)


@admin.register(SmartQRScan)
class SmartQRScanAdmin(admin.ModelAdmin):
    list_display = ('code', 'created_at', 'country', 'device_type', 'os_family', 'browser_family')
    readonly_fields = [field.name for field in SmartQRScan._meta.fields]
    search_fields = ('code__slug', 'country', 'browser_family', 'os_family', 'device_type')
    list_filter = ('country', 'device_type', 'os_family', 'browser_family', 'is_bot', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
