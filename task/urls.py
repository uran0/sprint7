from django.urls import path
from .views import new_task, task_created_success, welcome_page, task_list, my_tasks, delete_task, edit_task, task_edit_success

urlpatterns = [
    path('new_task/', new_task, name='new_task'),
    path('task_created_success/', task_created_success, name='task_created_success'),
    path('task_list/', task_list, name='task_list'),
    path('my_tasks/', my_tasks, name='my_tasks'),
    path('delete_task/<int:task_id>/', delete_task, name='delete_task'),
    path('task/<int:task_id>/', edit_task, name='edit_task'),
    path('task_edit_success/', task_edit_success, name='task_edit_success'),
    path('welcome/', welcome_page, name='welcome_page'), 
]
