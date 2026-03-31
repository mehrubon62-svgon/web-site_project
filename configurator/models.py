from django.db import models
from my_site_register.models import UniqUser
from my_site_app.models import Processor, GPU, RAM, Motherboard, Storage, PowerSupply, Case


class PCConfiguration(models.Model):
    """Конфигурации ПК"""
    user = models.ForeignKey(UniqUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="User")
    name = models.CharField(max_length=200, verbose_name="Configuration Name")
    
    # Компоненты
    processor = models.ForeignKey(Processor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Processor")
    gpu = models.ForeignKey(GPU, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="GPU")
    motherboard = models.ForeignKey(Motherboard, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Motherboard")
    ram = models.ForeignKey(RAM, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="RAM")
    power_supply = models.ForeignKey(PowerSupply, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Power Supply")
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Case")
    storage_devices = models.ManyToManyField(Storage, blank=True, verbose_name="Storage Devices")
    
    # Метаданные
    is_public = models.BooleanField(default=False, verbose_name="Public")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "PC Configuration"
        verbose_name_plural = "PC Configurations"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.username if self.user else 'Guest'}"
    
    def calculate_total_power(self):
        """Расчет общего энергопотребления в Ваттах"""
        power = 0
        
        # CPU
        if self.processor:
            power += self.processor.tdp_max
        
        # GPU
        if self.gpu:
            power += self.gpu.power_consumption
        
        # Motherboard
        if self.motherboard:
            power += self.motherboard.power_consumption
        
        # RAM
        if self.ram:
            power += self.ram.power_per_module * self.ram.modules
        
        # Storage devices
        for storage in self.storage_devices.all():
            power += storage.power_consumption
        
        # Фиксированные компоненты
        power += 15  # Охлаждение
        power += 20  # Вентиляторы
        power += 50  # USB устройства и периферия
        
        return power
    
    def get_recommended_psu_wattage(self):
        """Рекомендуемая мощность блока питания с запасом 25%"""
        total = self.calculate_total_power()
        recommended = total * 1.25  # Запас 25%
        
        # Округляем до стандартных значений БП
        standard_wattages = [450, 550, 650, 750, 850, 1000, 1200, 1500]
        for wattage in standard_wattages:
            if wattage >= recommended:
                return wattage
        return 1500
    
    def calculate_total_price(self):
        """Расчет общей стоимости конфигурации"""
        total = 0
        
        if self.processor:
            total += self.processor.price
        if self.gpu:
            total += self.gpu.price
        if self.motherboard:
            total += self.motherboard.price
        if self.ram:
            total += self.ram.price
        if self.power_supply:
            total += self.power_supply.price
        if self.case:
            total += self.case.price
        
        for storage in self.storage_devices.all():
            total += storage.price
        
        return total
    
    def check_compatibility(self):
        """Проверка совместимости компонентов. Возвращает список проблем."""
        issues = []
        
        # Проверка сокета CPU и материнской платы
        if self.processor and self.motherboard:
            if self.processor.socket != self.motherboard.socket:
                issues.append(f"⚠️ Socket incompatibility: CPU {self.processor.socket} != MB {self.motherboard.socket}")
        
        # Проверка типа памяти
        if self.ram and self.motherboard:
            if self.ram.memory_type != self.motherboard.ram_type:
                issues.append(f"⚠️ RAM incompatibility: RAM {self.ram.memory_type} != MB {self.motherboard.ram_type}")
        
        # Проверка мощности БП
        if self.power_supply:
            recommended = self.get_recommended_psu_wattage()
            if self.power_supply.wattage < recommended:
                issues.append(f"⚠️ Insufficient PSU power: {self.power_supply.wattage}W < {recommended}W (recommended)")
            elif self.power_supply.wattage < self.calculate_total_power():
                issues.append(f"❌ CRITICAL: PSU too weak! {self.power_supply.wattage}W < {self.calculate_total_power()}W (minimum)")
        
        # Проверка длины видеокарты и корпуса
        if self.gpu and self.case:
            if self.gpu.length > self.case.max_gpu_length:
                issues.append(f"⚠️ GPU won't fit in case: {self.gpu.length}mm > {self.case.max_gpu_length}mm")
        
        # Проверка форм-фактора материнской платы и корпуса
        if self.motherboard and self.case:
            # Упрощенная проверка (можно расширить)
            mb_ff = self.motherboard.form_factor
            case_ff = self.case.form_factor
            
            # ATX корпус поддерживает ATX, Micro-ATX, Mini-ITX
            # Micro-ATX корпус поддерживает Micro-ATX, Mini-ITX
            # Mini-ITX корпус поддерживает только Mini-ITX
            incompatible = False
            
            if case_ff == 'MINI_ITX' and mb_ff != 'MINI_ITX':
                incompatible = True
            elif case_ff == 'MICRO_ATX' and mb_ff in ['ATX', 'E_ATX']:
                incompatible = True
            
            if incompatible:
                issues.append(f"⚠️ Motherboard {mb_ff} won't fit in {case_ff} case")
        
        return issues
    
    def is_compatible(self):
        """Проверка: есть ли критические проблемы совместимости"""
        issues = self.check_compatibility()
        # Критические проблемы начинаются с ❌
        critical_issues = [issue for issue in issues if issue.startswith('❌')]
        return len(critical_issues) == 0
