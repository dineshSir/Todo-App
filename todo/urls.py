from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('tasks/', views.task_list, name='task_list'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_task, name='add_task'),
    path('delete/<int:id>', views.delete_task, name='delete_task'),
    path('edit/<int:id>', views.edit_task, name='edit_task'),
    path('completed/<int:id>', views.completed, name="completed"),
    path('test/', views.test_view, name='test'),
]
