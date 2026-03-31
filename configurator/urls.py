from django.urls import path
from .views import (
    ConfiguratorView,
    SavedConfigurationsView,
    SaveConfigurationView,
    AddCurrentBuildToCartView,
    AddSavedConfigurationToCartView,
    DeleteSavedConfigurationView,
)

urlpatterns = [
    path('configurator/', ConfiguratorView.as_view(), name='configurator'),
    path('configurator/save/', SaveConfigurationView.as_view(), name='save_configuration'),
    path('configurator/add-to-cart/', AddCurrentBuildToCartView.as_view(), name='add_current_build_to_cart'),
    path('configurations/', SavedConfigurationsView.as_view(), name='saved_configurations'),
    path('configurations/<int:pk>/add-to-cart/', AddSavedConfigurationToCartView.as_view(), name='add_saved_configuration_to_cart'),
    path('configurations/<int:pk>/delete/', DeleteSavedConfigurationView.as_view(), name='delete_saved_configuration'),
]
