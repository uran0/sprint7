from django.urls import path
from .views import new_task, task_created_success, welcome_page, task_list, my_tasks

urlpatterns = [
    path('new_task/', new_task, name='new_task'),
    path('task_created_success/', task_created_success, name='task_created_success'),
    path('task_list/', task_list, name='task_list'),
    path('my_tasks/', my_tasks, name='my_tasks'),
    #path('task/<int:task_id>/', task_detail, name='task_detail'),
    path('welcome/', welcome_page, name='welcome_page'), 
]
