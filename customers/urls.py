from django.urls import path
from . import views
from .views import get_item_price


urlpatterns = [
    # Customer CRUD routes (for context)
    path('', views.customer_list, name='customer_list'),
    path('add/', views.customer_create, name='customer_create'),
    path('<int:pk>/', views.customer_detail, name='customer_detail'),
    path('edit/<int:pk>/', views.customer_update, name='customer_update'),
    path('delete/<int:pk>/', views.customer_delete, name='customer_delete'),
    
    # Purchase CRUD routes
    path('purchase/', views.purchase_list, name='purchase_list'),
    path('purchase/add/', views.purchase_create, name='purchase_create'),
    path('purchase/<int:pk>/', views.purchase_detail, name='purchase_detail'),
    path('purchase/edit/<int:pk>/', views.purchase_update, name='purchase_update'),
    path('purchase/delete/<int:pk>/', views.purchase_delete, name='purchase_delete'),
]


# APIS
urlpatterns += [
    path('ajax/get-item-price/', get_item_price, name='get_item_price'),
]