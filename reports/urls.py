from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_index, name='reports_index'),
    path('inventory/', views.inventory_summary, name='inventory_summary'),
    path('purchases/', views.purchase_summary, name='purchase_summary'),
    path('financial/', views.financial_summary, name='financial_summary'),
]
