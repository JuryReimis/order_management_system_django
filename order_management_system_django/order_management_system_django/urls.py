from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

from order_management_system_django import settings

urlpatterns = [
    path('orders/', include('orders.urls')),
    path('carte/', include('carte.urls')),
    path('', include('carte.api.v1.urls')),
    path('', include('orders.api.v1.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url=reverse_lazy('orders:create_order')))
]

if settings.DEBUG is True:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
