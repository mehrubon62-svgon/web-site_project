from django.contrib import admin
from django.utils.html import format_html
from .models import ChatSession, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    fields = ('role', 'content_preview', 'created_at')
    readonly_fields = ('content_preview', 'created_at')
    can_delete = False
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Message'


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id_short', 'user_display', 'message_count', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('session_id', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ChatMessageInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user').prefetch_related('messages')
    
    def session_id_short(self, obj):
        return obj.session_id[:16] + '...' if len(obj.session_id) > 16 else obj.session_id
    session_id_short.short_description = 'Session ID'
    
    def user_display(self, obj):
        if obj.user:
            return format_html('<span style="color: #10B981; font-weight: bold;">{}</span>', obj.user.username)
        return format_html('<span style="color: #6B7280;">Guest</span>')
    user_display.short_description = 'User'
    
    def message_count(self, obj):
        count = obj.messages.count()
        return format_html('<span style="font-weight: bold;">{} messages</span>', count)
    message_count.short_description = 'Messages'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_short', 'role_display', 'content_preview', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('content', 'session__session_id')
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('session', 'session__user')
    
    def session_short(self, obj):
        if obj.session.user:
            return f"{obj.session.user.username}'s chat"
        return f"Guest {obj.session.session_id[:8]}"
    session_short.short_description = 'Session'
    
    def role_display(self, obj):
        colors = {
            'USER': '#3B82F6',      # Blue
            'ASSISTANT': '#10B981',  # Green
            'SYSTEM': '#6B7280',     # Gray
        }
        color = colors.get(obj.role, '#6B7280')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_role_display()
        )
    role_display.short_description = 'Role'
    
    def content_preview(self, obj):
        preview = obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
        return preview
    content_preview.short_description = 'Content'
