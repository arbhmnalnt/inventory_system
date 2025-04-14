from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # custom authentication views
    path('inventory/', include('inventory.urls')),
    path('financial/', include('financial.urls')),
    path('customers/', include('customers.urls')),
    path('reports/', include('reports.urls')),
    path('', include('accounts.urls')),  # redirect root to login or dashboard
]
