from django.contrib import admin
from django.utils.html import format_html
from .models import PCConfiguration


@admin.register(PCConfiguration)
class PCConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'total_price_display', 'total_power_display', 'compatibility_status', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('name', 'user__username')
    filter_horizontal = ('storage_devices',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'name', 'is_public')
        }),
        ('Components', {
            'fields': ('processor', 'gpu', 'motherboard', 'ram', 'power_supply', 'case', 'storage_devices')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'processor', 'gpu', 'motherboard', 'ram', 'power_supply', 'case').prefetch_related('storage_devices')
    
    def total_price_display(self, obj):
        total = obj.calculate_total_price()
        return format_html('<span style="font-weight: bold; color: #FBBF24;">${}</span>', total)
    total_price_display.short_description = 'Total Price'
    
    def total_power_display(self, obj):
        power = obj.calculate_total_power()
        recommended = obj.get_recommended_psu_wattage()
        
        if obj.power_supply:
            if obj.power_supply.wattage >= recommended:
                color = '#10B981'  # Green
            elif obj.power_supply.wattage >= power:
                color = '#F59E0B'  # Orange
            else:
                color = '#EF4444'  # Red
        else:
            color = '#6B7280'  # Gray
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}W / {}W recommended</span>',
            color, power, recommended
        )
    total_power_display.short_description = 'Power'
    
    def compatibility_status(self, obj):
        issues = obj.check_compatibility()
        if not issues:
            return format_html('<span style="color: #10B981; font-weight: bold;">✓ Compatible</span>')
        
        critical = [i for i in issues if i.startswith('❌')]
        warnings = [i for i in issues if i.startswith('⚠️')]
        
        if critical:
            return format_html(
                '<span style="color: #EF4444; font-weight: bold;">✗ {} critical issues</span>',
                len(critical)
            )
        else:
            return format_html(
                '<span style="color: #F59E0B; font-weight: bold;">⚠ {} warnings</span>',
                len(warnings)
            )
    compatibility_status.short_description = 'Compatibility'
