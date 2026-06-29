from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.get_todos, name='get_todos'),
    path('todos/create/', views.create_todo, name='create_todo'),
    path('todos/update/<int:todo_id>/', views.update_todo, name = 'update_todo'),
    path('todo/delete/<int:todo_id>/', views.delete_todo, name = 'delete_todo'),
]