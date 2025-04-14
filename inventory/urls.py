from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_item_list, name='inventory_item_list'),
    path('item/add/', views.inventory_item_create, name='inventory_item_create'),
    path('item/edit/<int:pk>/', views.inventory_item_update, name='inventory_item_update'),
    path('item/delete/<int:pk>/', views.inventory_item_delete, name='inventory_item_delete'),
    
    path('transactions/', views.inventory_transaction_list, name='inventory_transaction_list'),
    path('transactions/add/', views.inventory_transaction_create, name='inventory_transaction_create'),
]
