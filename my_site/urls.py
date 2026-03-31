from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('my_site_register.urls')) ,
    path('main_site/' , include('my_site_app.urls')),
    path('main_site/', include('configurator.urls')),
    path('main_site/', include('orders.urls')),
    path('main_site/', include('reviews.urls')),
    path('main_site/ai-chat/', include('ai_consultant.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
