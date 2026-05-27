from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('complete/<int:task_id>/', views.complete_task, name='complete'),
    path('delete/<int:task_id>/', views.delete_task, name='delete'),
    path('edit/<int:task_id>/', views.edit_task, name='edit'),
    path('recover/<int:task_id>/', views.recover_task, name='recover'),
    path('complete_all/', views.complete_all, name='complete_all'),
    path('search/', views.search_tasks, name='search_tasks'),


]

