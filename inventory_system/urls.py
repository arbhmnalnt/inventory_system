from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # custom authentication views
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('inventory/', include('inventory.urls')),
    path('financial/', include('financial.urls')),
    path('customers/', include('customers.urls')),
    path('reports/', include('reports.urls')),
    path('', include('accounts.urls')),  # redirect root to login or dashboard

]
