from django.db import models
from my_site_register.models import UniqUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# ==================== КОМПОНЕНТЫ ПК ====================

class Processor(models.Model):
    """Процессоры"""
    name = models.CharField(max_length=200, verbose_name="Name")
    manufacturer = models.CharField(max_length=100, verbose_name="Manufacturer")  # Intel, AMD
    socket = models.CharField(max_length=50, verbose_name="Socket")  # LGA1700, AM5
    cores = models.IntegerField(verbose_name="Cores")
    threads = models.IntegerField(verbose_name="Threads")
    base_clock = models.FloatField(verbose_name="Base Clock (GHz)")
    boost_clock = models.FloatField(verbose_name="Boost Clock (GHz)")
    tdp_base = models.IntegerField(verbose_name="TDP Base (W)")
    tdp_max = models.IntegerField(verbose_name="TDP Max (W)")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    image = models.ImageField(upload_to='processors/', blank=True, verbose_name="Main Image")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Processor"
        verbose_name_plural = "Processors"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.manufacturer} {self.name}"


class GPU(models.Model):
    """Видеокарты"""
    name = models.CharField(max_length=200, verbose_name="Name")
    manufacturer = models.CharField(max_length=100, verbose_name="Manufacturer")  # NVIDIA, AMD
    chipset = models.CharField(max_length=100, verbose_name="Chipset")  # RTX 4080, RX 7900 XT
    vram = models.IntegerField(verbose_name="VRAM (GB)")
    vram_type = models.CharField(max_length=50, verbose_name="VRAM Type")  # GDDR6, GDDR6X
    power_consumption = models.IntegerField(verbose_name="Power Consumption (W)")
    recommended_psu = models.IntegerField(verbose_name="Recommended PSU (W)")
    pcie_slots = models.IntegerField(default=2, verbose_name="PCIe Slots")
    length = models.IntegerField(verbose_name="Length (mm)")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    image = models.ImageField(upload_to='gpus/', blank=True, verbose_name="Main Image")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "GPU"
        verbose_name_plural = "GPUs"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.manufacturer} {self.name}"


class RAM(models.Model):
    """Оперативная память"""
    DDR_TYPES = [
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Name")
    manufacturer = models.CharField(max_length=100, verbose_name="Manufacturer")
    memory_type = models.CharField(max_length=20, choices=DDR_TYPES, verbose_name="Memory Type")
    capacity = models.IntegerField(verbose_name="Capacity per Module (GB)")
    modules = models.IntegerField(verbose_name="Number of Modules")
    speed = models.IntegerField(verbose_name="Speed (MHz)")
    power_per_module = models.IntegerField(default=5, verbose_name="Power per Module (W)")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    image = models.ImageField(upload_to='ram/', blank=True, verbose_name="Main Image")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "RAM"
        verbose_name_plural = "RAM"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.manufacturer} {self.name} {self.capacity}GB x{self.modules}"
    
    @property
    def total_capacity(self):
        """Общий объем памяти в комплекте"""
        return self.capacity * self.modules


class Motherboard(models.Model):
    """Материнские платы"""
    FORM_FACTORS = [
        ('ATX', 'ATX'),
        ('MICRO_ATX', 'Micro-ATX'),
        ('MINI_ITX', 'Mini-ITX'),
        ('E_ATX', 'E-ATX'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Name")
    manufacturer = models.CharField(max_length=100, verbose_name="Manufacturer")
    socket = models.CharField(max_length=50, verbose_name="Socket")  # LGA1700, AM5
    chipset = models.CharField(max_length=50, verbose_name="Chipset")  # Z790, B650
    form_factor = models.CharField(max_length=20, choices=FORM_FACTORS, verbose_name="Form Factor")
    ram_type = models.CharField(max_length=20, verbose_name="RAM Type")  # DDR4, DDR5
    ram_slots = models.IntegerField(verbose_name="RAM Slots")
    max_ram = models.IntegerField(verbose_name="Max RAM (GB)")
    m2_slots = models.IntegerField(verbose_name="M.2 Slots")
    sata_ports = models.IntegerField(verbose_name="SATA Ports")
    pcie_x16_slots = models.IntegerField(verbose_name="PCIe x16 Slots")
    power_consumption = models.IntegerField(default=80, verbose_name="Power Consumption (W)")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    image = models.ImageField(upload_to='motherboards/', blank=True, verbose_name="Main Image")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Motherboard"
        verbose_name_plural = "Motherboards"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.manufacturer} {self.name}"


class Storage(models.Model):
    """Накопители"""
    STORAGE_TYPES = [
        ('NVME', 'NVMe SSD'),
        ('SATA_SSD', 'SATA SSD'),
        ('HDD', 'HDD'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Name")
    manufacturer = models.CharField(max_length=100, verbose_name="Manufacturer")
    storage_type = models.CharField(max_length=20, choices=STORAGE_TYPES, verbose_name="Storage Type")
    capacity = models.IntegerField(verbose_name="Capacity (GB)")
    read_speed = models.IntegerField(null=True, blank=True, verbose_name="Read Speed (MB/s)")
    write_speed = models.IntegerField(null=True, blank=True, verbose_name="Write Speed (MB/s)")
    power_consumption = models.IntegerField(verbose_name="Power Consumption (W)")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    image = models.ImageField(upload_to='storage/', blank=True, verbose_name="Main Image")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Storage"
        verbose_name_plural = "Storage"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.manufacturer} {self.name} {self.capacity}GB"


class PowerSupply(models.Model):
    """Блоки питания"""
    EFFICIENCY_RATINGS = [
        ('80PLUS', '80 Plus'),
        ('BRONZE', '80 Plus Bronze'),
        ('SILVER', '80 Plus Silver'),
        ('GOLD', '80 Plus Gold'),
        ('PLATINUM', '80 Plus Platinum'),
        ('TITANIUM', '80 Plus Titanium'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Name")
    manufacturer = models.CharField(max_length=100, verbose_name="Manufacturer")
    wattage = models.IntegerField(verbose_name="Wattage (W)")
    efficiency = models.CharField(max_length=20, choices=EFFICIENCY_RATINGS, verbose_name="Efficiency Rating")
    modular = models.BooleanField(default=False, verbose_name="Modular")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    image = models.ImageField(upload_to='psu/', blank=True, verbose_name="Main Image")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Power Supply"
        verbose_name_plural = "Power Supplies"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.manufacturer} {self.name} {self.wattage}W"


class Case(models.Model):
    """Корпуса"""
    FORM_FACTORS = [
        ('ATX', 'ATX'),
        ('MICRO_ATX', 'Micro-ATX'),
        ('MINI_ITX', 'Mini-ITX'),
        ('E_ATX', 'E-ATX'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Name")
    manufacturer = models.CharField(max_length=100, verbose_name="Manufacturer")
    form_factor = models.CharField(max_length=20, choices=FORM_FACTORS, verbose_name="Form Factor")
    max_gpu_length = models.IntegerField(verbose_name="Max GPU Length (mm)")
    max_cpu_cooler_height = models.IntegerField(verbose_name="Max CPU Cooler Height (mm)")
    fan_slots = models.IntegerField(verbose_name="Fan Slots")
    included_fans = models.IntegerField(default=0, verbose_name="Included Fans")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    image = models.ImageField(upload_to='cases/', blank=True, verbose_name="Main Image")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Case"
        verbose_name_plural = "Cases"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.manufacturer} {self.name}"


# ==================== НОУТБУКИ ====================

class Laptop(models.Model):
    """Ноутбуки"""
    CATEGORY_CHOICES = [
        ('GAMING', 'Gaming'),
        ('OFFICE', 'Office'),
        ('ULTRABOOK', 'Ultrabook'),
        ('WORKSTATION', 'Workstation'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Name")
    manufacturer = models.CharField(max_length=100, verbose_name="Manufacturer")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Category")
    
    # Характеристики
    processor_name = models.CharField(max_length=200, verbose_name="Processor")
    gpu_name = models.CharField(max_length=200, verbose_name="GPU")
    ram_size = models.IntegerField(verbose_name="RAM (GB)")
    ram_type = models.CharField(max_length=20, verbose_name="RAM Type")
    storage_size = models.IntegerField(verbose_name="Storage (GB)")
    storage_type = models.CharField(max_length=50, verbose_name="Storage Type")
    
    # Экран
    screen_size = models.FloatField(verbose_name="Screen Size (inches)")
    screen_resolution = models.CharField(max_length=50, verbose_name="Screen Resolution")
    screen_refresh_rate = models.IntegerField(default=60, verbose_name="Refresh Rate (Hz)")
    
    # Прочее
    weight = models.FloatField(verbose_name="Weight (kg)")
    battery_capacity = models.IntegerField(verbose_name="Battery Capacity (Wh)")
    power_consumption = models.IntegerField(default=65, verbose_name="Power Consumption (W)")
    
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    image = models.ImageField(upload_to='laptops/', blank=True, verbose_name="Main Image")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Laptop"
        verbose_name_plural = "Laptops"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.manufacturer} {self.name}"


# ==================== ДОПОЛНИТЕЛЬНЫЕ ИЗОБРАЖЕНИЯ ====================

class ProductImage(models.Model):
    """Дополнительные изображения для товаров"""
    # Универсальная связь с любым товаром через ContentType
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    image = models.ImageField(upload_to='product_images/', verbose_name="Image")
    is_main = models.BooleanField(default=False, verbose_name="Main Photo")
    order = models.IntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ['order']
    
    def __str__(self):
        return f"Photo #{self.order} for {self.content_object}"


class HomeHeroImage(models.Model):
    image = models.ImageField(upload_to='home_hero/', verbose_name="Hero Image")
    title = models.CharField(max_length=120, blank=True, default="")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Home Hero Image"
        verbose_name_plural = "Home Hero Images"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title or f"Hero Image #{self.pk}"


# ==================== WISHLIST (ИЗБРАННОЕ) ====================

class Wishlist(models.Model):
    """Избранное (только для авторизованных пользователей)"""
    user = models.ForeignKey(UniqUser, on_delete=models.CASCADE, verbose_name="User")
    
    # Универсальная связь с любым товаром
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlist"
        unique_together = ['user', 'content_type', 'object_id']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.content_object}"


class ExploreShowcaseItem(models.Model):
    """Элемент витрины mixed-browse (любой тип товара через Generic FK)."""
    title = models.CharField(max_length=200, blank=True, default="")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    position = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Explore Showcase Item"
        verbose_name_plural = "Explore Showcase Items"
        ordering = ["position", "-created_at"]

    def __str__(self):
        return self.title or f"Showcase #{self.pk}"


class ExploreLike(models.Model):
    """Лайк товара в общем разделе Explore."""
    user = models.ForeignKey(UniqUser, on_delete=models.CASCADE, verbose_name="User")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Explore Like"
        verbose_name_plural = "Explore Likes"
        unique_together = ["user", "content_type", "object_id"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} like {self.content_type.model}:{self.object_id}"


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    quantity = models.PositiveIntegerField(default=1, help_text="How many total times this promo can be used.")
    discount_percent = models.PositiveSmallIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.code

    @property
    def used_count(self):
        return self.usages.count()

    @property
    def remaining_quantity(self):
        remaining = self.quantity - self.used_count
        return max(0, remaining)


class PromoCodeUsage(models.Model):
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, related_name="usages")
    user = models.ForeignKey(UniqUser, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["promo_code", "user"]
        ordering = ["-used_at"]

    def __str__(self):
        return f"{self.user.username} used {self.promo_code.code}"


class UserSavedAddress(models.Model):
    user = models.OneToOneField(UniqUser, on_delete=models.CASCADE, related_name="saved_address")
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, default="")
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=120)
    region = models.CharField(max_length=120, blank=True, default="")
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=120, default="Tajikistan")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} address"
    
