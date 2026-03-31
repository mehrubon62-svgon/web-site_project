from django.urls import path 
from .views import *

urlpatterns = [
    path('home', Home.as_view(), name='home'),
    path('cart/', ShoppingCartView.as_view(), name='shopping_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('cart/add/<str:model_name>/<int:pk>/', AddCatalogItemToCartView.as_view(), name='cart_add'),
    path('explore/', ExploreAllView.as_view(), name='explore_all'),
    
    # Catalog pages
    path('catalog/processors/', ProcessorListView.as_view(), name='processors'),
    path('catalog/gpus/', GPUListView.as_view(), name='gpus'),
    path('catalog/ram/', RAMListView.as_view(), name='ram'),
    path('catalog/motherboards/', MotherboardListView.as_view(), name='motherboards'),
    path('catalog/storage/', StorageListView.as_view(), name='storage'),
    path('catalog/power-supplies/', PowerSupplyListView.as_view(), name='power_supplies'),
    path('catalog/cases/', CaseListView.as_view(), name='cases'),
    path('catalog/laptops/', LaptopListView.as_view(), name='laptops'),
    
    # Product detail pages
    path('processor/<int:pk>/', ProcessorDetailView.as_view(), name='processor_detail'),
    path('gpu/<int:pk>/', GPUDetailView.as_view(), name='gpu_detail'),
    path('ram/<int:pk>/', RAMDetailView.as_view(), name='ram_detail'),
    path('motherboard/<int:pk>/', MotherboardDetailView.as_view(), name='motherboard_detail'),
    path('storage/<int:pk>/', StorageDetailView.as_view(), name='storage_detail'),
    path('power-supply/<int:pk>/', PowerSupplyDetailView.as_view(), name='power_supply_detail'),
    path('case/<int:pk>/', CaseDetailView.as_view(), name='case_detail'),
    path('laptop/<int:pk>/', LaptopDetailView.as_view(), name='laptop_detail'),

    # Wishlist
    path('wishlist/add/processor/<int:pk>/', AddWishProcessor.as_view(), name='add_wish_processor'),
    path('wishlist/add/gpu/<int:pk>/', AddWishGPU.as_view(), name='add_wish_gpu'),
    path('wishlist/add/ram/<int:pk>/', AddWishRAM.as_view(), name='add_wish_ram'),
    path('wishlist/add/motherboard/<int:pk>/', AddWishMotherboard.as_view(), name='add_wish_motherboard'),
    path('wishlist/add/storage/<int:pk>/', AddWishStorage.as_view(), name='add_wish_storage'),
    path('wishlist/add/power-supply/<int:pk>/', AddWishPowerSupply.as_view(), name='add_wish_power_supply'),
    path('wishlist/add/case/<int:pk>/', AddWishCase.as_view(), name='add_wish_case'),
    path('wishlist/add/laptop/<int:pk>/', AddWishLaptop.as_view(), name='add_wish_laptop'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/<int:pk>/remove/', RemoveWishlistItemView.as_view(), name='wishlist_remove'),
    path('wishlist/<int:pk>/add-to-cart/', AddWishlistItemToCartView.as_view(), name='wishlist_add_to_cart'),
    path('explore/like-toggle/', ToggleExploreLikeView.as_view(), name='toggle_explore_like'),
    path('explore/wishlist-toggle/', ToggleWishlistAjaxView.as_view(), name='toggle_wishlist_ajax'),
]
