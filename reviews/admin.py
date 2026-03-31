from django.contrib import admin
from django.utils.html import format_html
from .models import Review, ReviewReply


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'rating_display', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('user__username', 'comment')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Review Info', {
            'fields': ('user', 'content_type', 'object_id', 'rating', 'comment')
        }),
        ('Moderation', {
            'fields': ('is_approved',)
        }),
        ('Dates', {
            'fields': ('created_at',)
        }),
    )
    
    def rating_display(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: #FBBF24; font-size: 16px;">{}</span>', stars)
    rating_display.short_description = 'Rating'
    
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} reviews approved")
    approve_reviews.short_description = "Approve selected reviews"
    
    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"{queryset.count()} reviews disapproved")
    disapprove_reviews.short_description = "Disapprove selected reviews"


@admin.register(ReviewReply)
class ReviewReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'created_at')
    search_fields = ('user__username', 'comment')
    readonly_fields = ('created_at',)
