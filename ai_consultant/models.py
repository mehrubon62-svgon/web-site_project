from django.db import models
from my_site_register.models import UniqUser


class ChatSession(models.Model):
    """Сессия чата с AI-консультантом"""
    user = models.ForeignKey(UniqUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="User")
    session_id = models.CharField(max_length=100, unique=True, verbose_name="Session ID")  # Для гостей
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Chat Session"
        verbose_name_plural = "Chat Sessions"
        ordering = ['-updated_at']
    
    def __str__(self):
        if self.user:
            return f"Chat {self.user.username}"
        return f"Guest Chat {self.session_id[:8]}"


class ChatMessage(models.Model):
    """Сообщения в чате с AI""" 
    ROLE_CHOICES = [
        ('USER', 'User'),
        ('ASSISTANT', 'AI Consultant'),
        ('SYSTEM', 'System'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages', verbose_name="Session")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="Role")
    content = models.TextField(verbose_name="Message Content")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Chat Message"
        verbose_name_plural = "Chat Messages"
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.get_role_display()}: {self.content[:50]}..."
