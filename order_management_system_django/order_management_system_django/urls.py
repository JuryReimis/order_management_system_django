from django.contrib import admin
from django.urls import path, include

from order_management_system_django import settings

urlpatterns = [
    path('orders/', include('orders.urls')),
    path('carte/', include('carte.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG is True:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
