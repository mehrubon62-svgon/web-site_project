from django.db import models
from my_site_register.models import UniqUser
from configurator.models import PCConfiguration


class Order(models.Model):
    """Заказы"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(UniqUser, on_delete=models.CASCADE, verbose_name="User")
    configuration = models.ForeignKey(PCConfiguration, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="PC Configuration")
    
    # Можно также заказать отдельные товары (не только конфигурацию)
    # Для этого можно добавить ManyToMany к товарам или использовать OrderItem
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Status")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")
    
    # Данные доставки
    full_name = models.CharField(max_length=200, verbose_name="Full Name")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    email = models.EmailField(verbose_name="Email")
    address = models.TextField(verbose_name="Delivery Address")
    
    # Комментарий к заказу
    comment = models.TextField(blank=True, verbose_name="Comment")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username} ({self.get_status_display()})"
