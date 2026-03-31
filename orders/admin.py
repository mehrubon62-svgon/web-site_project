from django.contrib import admin
from django.utils.html import format_html
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status_display', 'total_price', 'full_name', 'phone', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'full_name', 'email', 'phone', 'id')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'configuration', 'status', 'total_price')
        }),
        ('Customer Info', {
            'fields': ('full_name', 'phone', 'email', 'address', 'comment')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'configuration')
    
    def status_display(self, obj):
        colors = {
            'PENDING': '#F59E0B',      # Orange
            'PROCESSING': '#3B82F6',   # Blue
            'SHIPPED': '#8B5CF6',      # Purple
            'DELIVERED': '#10B981',    # Green
            'CANCELLED': '#EF4444',    # Red
        }
        color = colors.get(obj.status, '#6B7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    def mark_as_processing(self, request, queryset):
        queryset.update(status='PROCESSING')
        self.message_user(request, f"{queryset.count()} orders marked as Processing")
    mark_as_processing.short_description = "Mark as Processing"
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='SHIPPED')
        self.message_user(request, f"{queryset.count()} orders marked as Shipped")
    mark_as_shipped.short_description = "Mark as Shipped"
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='DELIVERED')
        self.message_user(request, f"{queryset.count()} orders marked as Delivered")
    mark_as_delivered.short_description = "Mark as Delivered"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='CANCELLED')
        self.message_user(request, f"{queryset.count()} orders marked as Cancelled")
    mark_as_cancelled.short_description = "Mark as Cancelled"
