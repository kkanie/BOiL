from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.create_task),
    path('calculate/', views.calculate_critical_path),
]