from django.db import models
from my_site_register.models import UniqUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Review(models.Model):
    """Отзывы на товары"""
    user = models.ForeignKey(UniqUser, on_delete=models.CASCADE, verbose_name="User")
    
    # Универсальная связь с любым товаром (процессор, видеокарта, ноутбук и т.д.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    rating = models.IntegerField(verbose_name="Rating (1-5)")
    comment = models.TextField(verbose_name="Comment")
    
    # Модерация
    is_approved = models.BooleanField(default=True, verbose_name="Approved")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']
        # Один пользователь может оставить только один отзыв на товар
        unique_together = ['user', 'content_type', 'object_id']
    
    def __str__(self):
        return f"Review from {self.user.username} - {self.rating}/5 on {self.content_object}"
    
    def clean(self):
        """Валидация рейтинга"""
        from django.core.exceptions import ValidationError
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5')


class ReviewReply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(UniqUser, on_delete=models.CASCADE, verbose_name="User")
    comment = models.TextField(verbose_name="Reply")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review Reply"
        verbose_name_plural = "Review Replies"
        ordering = ['created_at']

    def __str__(self):
        return f"Reply from {self.user.username} on review #{self.review_id}"
