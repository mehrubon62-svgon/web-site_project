from django.contrib import admin
from django.utils.html import format_html
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import (
    Processor, GPU, RAM, Motherboard, Storage, PowerSupply, Case,
    Laptop, ProductImage, HomeHeroImage, Wishlist, PromoCode, PromoCodeUsage, UserSavedAddress
)


# ==================== PRODUCT IMAGE INLINE ====================
class ProductImageInline(GenericTabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_main', 'order', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


# ==================== PROCESSOR ADMIN ====================
@admin.register(Processor)
class ProcessorAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'socket', 'cores', 'threads', 'price', 'stock_status', 'main_image_preview')
    list_filter = ('manufacturer', 'socket', 'cores')
    search_fields = ('name', 'manufacturer')
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'manufacturer', 'image', 'description')
        }),
        ('Specifications', {
            'fields': ('socket', 'cores', 'threads', 'base_clock', 'boost_clock', 'tdp_base', 'tdp_max')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
    )
    
    def stock_status(self, obj):
        if obj.stock > 10:
            color = '#10B981'
            text = f'✓ In Stock ({obj.stock})'
        elif obj.stock > 0:
            color = '#F59E0B'
            text = f'⚠ Low Stock ({obj.stock})'
        else:
            color = '#EF4444'
            text = '✗ Out of Stock'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, text)
    stock_status.short_description = 'Stock'
    
    def main_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No image"
    main_image_preview.short_description = 'Image'


# ==================== GPU ADMIN ====================
@admin.register(GPU)
class GPUAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'chipset', 'vram', 'power_consumption', 'price', 'stock_status', 'main_image_preview')
    list_filter = ('manufacturer', 'vram', 'vram_type')
    search_fields = ('name', 'manufacturer', 'chipset')
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'manufacturer', 'chipset', 'image', 'description')
        }),
        ('Specifications', {
            'fields': ('vram', 'vram_type', 'power_consumption', 'recommended_psu', 'pcie_slots', 'length')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
    )
    
    def stock_status(self, obj):
        if obj.stock > 10:
            color = '#10B981'
            text = f'✓ In Stock ({obj.stock})'
        elif obj.stock > 0:
            color = '#F59E0B'
            text = f'⚠ Low Stock ({obj.stock})'
        else:
            color = '#EF4444'
            text = '✗ Out of Stock'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, text)
    stock_status.short_description = 'Stock'
    
    def main_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No image"
    main_image_preview.short_description = 'Image'


# ==================== RAM ADMIN ====================
@admin.register(RAM)
class RAMAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'memory_type', 'total_capacity_display', 'speed', 'price', 'stock_status', 'main_image_preview')
    list_filter = ('manufacturer', 'memory_type', 'capacity')
    search_fields = ('name', 'manufacturer')
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'manufacturer', 'image', 'description')
        }),
        ('Specifications', {
            'fields': ('memory_type', 'capacity', 'modules', 'speed', 'power_per_module')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
    )
    
    def total_capacity_display(self, obj):
        return f"{obj.total_capacity}GB ({obj.capacity}GB × {obj.modules})"
    total_capacity_display.short_description = 'Total Capacity'
    
    def stock_status(self, obj):
        if obj.stock > 10:
            color = '#10B981'
            text = f'✓ In Stock ({obj.stock})'
        elif obj.stock > 0:
            color = '#F59E0B'
            text = f'⚠ Low Stock ({obj.stock})'
        else:
            color = '#EF4444'
            text = '✗ Out of Stock'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, text)
    stock_status.short_description = 'Stock'
    
    def main_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No image"
    main_image_preview.short_description = 'Image'


# ==================== MOTHERBOARD ADMIN ====================
@admin.register(Motherboard)
class MotherboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'socket', 'chipset', 'form_factor', 'ram_type', 'price', 'stock_status', 'main_image_preview')
    list_filter = ('manufacturer', 'socket', 'form_factor', 'ram_type')
    search_fields = ('name', 'manufacturer', 'chipset')
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'manufacturer', 'image', 'description')
        }),
        ('Specifications', {
            'fields': ('socket', 'chipset', 'form_factor', 'ram_type', 'ram_slots', 'max_ram', 'm2_slots', 'sata_ports', 'pcie_x16_slots', 'power_consumption')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
    )
    
    def stock_status(self, obj):
        if obj.stock > 10:
            color = '#10B981'
            text = f'✓ In Stock ({obj.stock})'
        elif obj.stock > 0:
            color = '#F59E0B'
            text = f'⚠ Low Stock ({obj.stock})'
        else:
            color = '#EF4444'
            text = '✗ Out of Stock'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, text)
    stock_status.short_description = 'Stock'
    
    def main_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No image"
    main_image_preview.short_description = 'Image'


# ==================== STORAGE ADMIN ====================
@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'storage_type', 'capacity_display', 'price', 'stock_status', 'main_image_preview')
    list_filter = ('manufacturer', 'storage_type')
    search_fields = ('name', 'manufacturer')
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'manufacturer', 'storage_type', 'image', 'description')
        }),
        ('Specifications', {
            'fields': ('capacity', 'read_speed', 'write_speed', 'power_consumption')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
    )
    
    def capacity_display(self, obj):
        if obj.capacity >= 1000:
            return f"{obj.capacity / 1000:.1f}TB"
        return f"{obj.capacity}GB"
    capacity_display.short_description = 'Capacity'
    
    def stock_status(self, obj):
        if obj.stock > 10:
            color = '#10B981'
            text = f'✓ In Stock ({obj.stock})'
        elif obj.stock > 0:
            color = '#F59E0B'
            text = f'⚠ Low Stock ({obj.stock})'
        else:
            color = '#EF4444'
            text = '✗ Out of Stock'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, text)
    stock_status.short_description = 'Stock'
    
    def main_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No image"
    main_image_preview.short_description = 'Image'


# ==================== POWER SUPPLY ADMIN ====================
@admin.register(PowerSupply)
class PowerSupplyAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'wattage', 'efficiency', 'modular', 'price', 'stock_status', 'main_image_preview')
    list_filter = ('manufacturer', 'efficiency', 'modular')
    search_fields = ('name', 'manufacturer')
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'manufacturer', 'image', 'description')
        }),
        ('Specifications', {
            'fields': ('wattage', 'efficiency', 'modular')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
    )
    
    def stock_status(self, obj):
        if obj.stock > 10:
            color = '#10B981'
            text = f'✓ In Stock ({obj.stock})'
        elif obj.stock > 0:
            color = '#F59E0B'
            text = f'⚠ Low Stock ({obj.stock})'
        else:
            color = '#EF4444'
            text = '✗ Out of Stock'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, text)
    stock_status.short_description = 'Stock'
    
    def main_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No image"
    main_image_preview.short_description = 'Image'


# ==================== CASE ADMIN ====================
@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'form_factor', 'max_gpu_length', 'price', 'stock_status', 'main_image_preview')
    list_filter = ('manufacturer', 'form_factor')
    search_fields = ('name', 'manufacturer')
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'manufacturer', 'form_factor', 'image', 'description')
        }),
        ('Specifications', {
            'fields': ('max_gpu_length', 'max_cpu_cooler_height', 'fan_slots', 'included_fans')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
    )
    
    def stock_status(self, obj):
        if obj.stock > 10:
            color = '#10B981'
            text = f'✓ In Stock ({obj.stock})'
        elif obj.stock > 0:
            color = '#F59E0B'
            text = f'⚠ Low Stock ({obj.stock})'
        else:
            color = '#EF4444'
            text = '✗ Out of Stock'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, text)
    stock_status.short_description = 'Stock'
    
    def main_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No image"
    main_image_preview.short_description = 'Image'


# ==================== LAPTOP ADMIN ====================
@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'category', 'processor_name', 'ram_size', 'price', 'stock_status', 'main_image_preview')
    list_filter = ('manufacturer', 'category', 'ram_size')
    search_fields = ('name', 'manufacturer', 'processor_name')
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'manufacturer', 'category', 'image', 'description')
        }),
        ('Hardware', {
            'fields': ('processor_name', 'gpu_name', 'ram_size', 'ram_type', 'storage_size', 'storage_type')
        }),
        ('Display', {
            'fields': ('screen_size', 'screen_resolution', 'screen_refresh_rate')
        }),
        ('Other', {
            'fields': ('weight', 'battery_capacity', 'power_consumption')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
    )
    
    def stock_status(self, obj):
        if obj.stock > 10:
            color = '#10B981'
            text = f'✓ In Stock ({obj.stock})'
        elif obj.stock > 0:
            color = '#F59E0B'
            text = f'⚠ Low Stock ({obj.stock})'
        else:
            color = '#EF4444'
            text = '✗ Out of Stock'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, text)
    stock_status.short_description = 'Stock'
    
    def main_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No image"
    main_image_preview.short_description = 'Image'


# ==================== PRODUCT IMAGE ADMIN ====================
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'is_main', 'order', 'image_preview', 'created_at')
    list_filter = ('is_main', 'created_at')
    search_fields = ('object_id',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(HomeHeroImage)
class HomeHeroImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'order', 'is_active', 'image_preview', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    list_editable = ('order', 'is_active')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="120" height="68" style="object-fit: cover; border-radius: 6px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


# ==================== WISHLIST ADMIN ====================
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'quantity', 'is_active', 'created_at')
    list_filter = ('is_active', 'discount_percent', 'created_at')
    search_fields = ('code',)


@admin.register(PromoCodeUsage)
class PromoCodeUsageAdmin(admin.ModelAdmin):
    list_display = ('promo_code', 'user', 'used_at')
    list_filter = ('promo_code', 'used_at')
    search_fields = ('promo_code__code', 'user__username')


@admin.register(UserSavedAddress)
class UserSavedAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'region', 'country', 'updated_at')
    search_fields = ('user__username', 'full_name', 'city', 'region')
