import django_filters
from .models import *


class ProcessorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Search by Name')
    manufacturer = django_filters.MultipleChoiceFilter(
        choices=[('Intel', 'Intel'), ('AMD', 'AMD')],
        widget=django_filters.widgets.forms.CheckboxSelectMultiple
    )
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock', label='In Stock')
    
    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset
    
    class Meta:
        model = Processor
        fields = ['name', 'manufacturer']


class GPUFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Search by Name')
    manufacturer = django_filters.MultipleChoiceFilter(
        choices=[('NVIDIA', 'NVIDIA'), ('AMD', 'AMD')],
        widget=django_filters.widgets.forms.CheckboxSelectMultiple
    )
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock', label='In Stock')
    
    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset
    
    class Meta:
        model = GPU
        fields = ['name', 'manufacturer']


class RAMFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Search by Name')
    manufacturer = django_filters.MultipleChoiceFilter(
        choices=[('Corsair', 'Corsair'), ('G.Skill', 'G.Skill'), ('Kingston', 'Kingston'), ('Crucial', 'Crucial'), ('TeamGroup', 'TeamGroup')],
        widget=django_filters.widgets.forms.CheckboxSelectMultiple
    )
    memory_type = django_filters.MultipleChoiceFilter(
        choices=RAM.DDR_TYPES,
        widget=django_filters.widgets.forms.CheckboxSelectMultiple
    )
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock', label='In Stock')
    
    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset
    
    class Meta:
        model = RAM
        fields = ['name', 'manufacturer', 'memory_type']


class MotherboardFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Search by Name')
    manufacturer = django_filters.MultipleChoiceFilter(
        choices=[('ASUS', 'ASUS'), ('MSI', 'MSI'), ('Gigabyte', 'Gigabyte'), ('ASRock', 'ASRock')],
        widget=django_filters.widgets.forms.CheckboxSelectMultiple
    )
    form_factor = django_filters.MultipleChoiceFilter(
        choices=Motherboard.FORM_FACTORS,
        widget=django_filters.widgets.forms.CheckboxSelectMultiple
    )
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock', label='In Stock')
    
    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset
    
    class Meta:
        model = Motherboard
        fields = ['name', 'manufacturer', 'form_factor']


class StorageFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Search by Name')
    manufacturer = django_filters.MultipleChoiceFilter(
        choices=[('Samsung', 'Samsung'), ('WD', 'WD'), ('Crucial', 'Crucial'), ('Kingston', 'Kingston'), ('Seagate', 'Seagate')],
        widget=django_filters.widgets.forms.CheckboxSelectMultiple
    )
    storage_type = django_filters.MultipleChoiceFilter(
        choices=Storage.STORAGE_TYPES,
        widget=django_filters.widgets.forms.CheckboxSelectMultiple
    )
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock', label='In Stock')
    
    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset
    
    class Meta:
        model = Storage
        fields = ['name', 'manufacturer', 'storage_type']


class PowerSupplyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Search by Name')
    manufacturer = django_filters.MultipleChoiceFilter(
        choices=[('Corsair', 'Corsair'), ('EVGA', 'EVGA'), ('Seasonic', 'Seasonic'), ('Thermaltake', 'Thermaltake'), ('Cooler Master', 'Cooler Master')],
        widget=django_filters.widgets.forms.CheckboxSelectMultiple
    )
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock', label='In Stock')
    
    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset
    
    class Meta:
        model = PowerSupply
        fields = ['name', 'manufacturer']


class CaseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Search by Name')
    manufacturer = django_filters.MultipleChoiceFilter(
        choices=[('Lian Li', 'Lian Li'), ('NZXT', 'NZXT'), ('Corsair', 'Corsair'), ('Fractal Design', 'Fractal Design'), ('Cooler Master', 'Cooler Master')],
        widget=django_filters.widgets.forms.CheckboxSelectMultiple
    )
    form_factor = django_filters.MultipleChoiceFilter(
        choices=Case.FORM_FACTORS,
        widget=django_filters.widgets.forms.CheckboxSelectMultiple
    )
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock', label='In Stock')
    
    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset
    
    class Meta:
        model = Case
        fields = ['name', 'manufacturer', 'form_factor']


class CoolerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Search by Name')
    manufacturer = django_filters.CharFilter(field_name='manufacturer', lookup_expr='icontains', label='Manufacturer')
    cooler_type = django_filters.MultipleChoiceFilter(
        choices=Cooler.COOLER_TYPES,
        widget=django_filters.widgets.forms.CheckboxSelectMultiple
    )
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock', label='In Stock')

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset

    class Meta:
        model = Cooler
        fields = ['name', 'manufacturer', 'cooler_type']


class LaptopFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Search by Name')
    manufacturer = django_filters.MultipleChoiceFilter(
        choices=[('Dell', 'Dell'), ('HP', 'HP'), ('Lenovo', 'Lenovo'), ('ASUS', 'ASUS'), ('MSI', 'MSI'), ('Acer', 'Acer')],
        widget=django_filters.widgets.forms.CheckboxSelectMultiple
    )
    category = django_filters.MultipleChoiceFilter(
        choices=Laptop.CATEGORY_CHOICES,
        widget=django_filters.widgets.forms.CheckboxSelectMultiple
    )
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock', label='In Stock')
    
    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset
    
    class Meta:
        model = Laptop
        fields = ['name', 'manufacturer', 'category']
