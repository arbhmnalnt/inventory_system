from django.urls import path
from . import views

urlpatterns = [
    path('', views.financial_list, name='financial_list'),
    path('create/', views.financial_create, name='financial_create'),
    path('update/<int:pk>/', views.financial_update, name='financial_update'),
    path('delete/<int:pk>/', views.financial_delete, name='financial_delete'),
]
