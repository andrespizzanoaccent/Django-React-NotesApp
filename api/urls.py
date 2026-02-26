from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name="routes"),
    path('notes/', views.getNotes, name="notes"),
    path('notes/<str:pk>/', views.getNote, name="note"),
    path('categories/', views.manageCategories, name="categories"),
    path('categories/<str:pk>/', views.manageCategory, name="category"),
]
