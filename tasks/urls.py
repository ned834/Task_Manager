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
    path("task/<int:task_id>/json/", views.task_json, name="task_json"),
    path("clear_completed/", views.clear_completed, name="clear_completed"),
    path("return_home/", views.return_home, name="return_home"),

]

