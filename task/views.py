from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django .utils.timezone import now
from .models import Status, Task, Tag, Priority
from account.models import User
from .forms import TaskForm, TaskModelForm
from django.urls import reverse
from django.core.exceptions import PermissionDenied
# Create your views here.

@login_required
def welcome_page(request):
    return render(request, "task/welcome_page.html")

@login_required
def new_task(request):
    if request.method == 'POST':
        form = TaskForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            assigned_user = data['assigned_to']
            priority_value = True if data['priority'] == 'alta' else False
            priority, _ = Priority.objects.get_or_create(priority=priority_value)
            task = Task.objects.create(
                user = assigned_user,
                name = data['name'],
                status = Status.objects.get(id=data['status']),
                tag = Tag.objects.get(id=data['tag']),
                description = data['description'] if data['description']!="" else "-sin información-",
                expire_date = data['expire_date'],
                priority = priority
            )
            task.save()
            return redirect("task_created_success")
    else:
        form = TaskForm()
    return render(request, "task/new_task.html", {'form': form})

@login_required
def task_created_success(request):
    return render(request, "task/task_created_success.html")
    

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task/task_list.html', {'tasks': tasks})
    
@login_required
def my_tasks(request):
    user = request.user
    tasks = Task.objects.filter(user=user)
    return render(request, 'task/my_tasks.html', {'tasks': tasks})


@login_required
def delete_task(request,task_id):
    try:
        task= get_object_or_404(Task, id=task_id)
        if not request.user.is_superuser:
            raise PermissionDenied
        task.delete()
        return redirect("task_list")
    except Task.DoesNotExist:
        return redirect("task_list")
    except PermissionDenied:
        messages.error(request, "Sólo los administradores puedes eliminar tareas.")
        return redirect("task_list")


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskModelForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_edit_success")
    else:
        form = TaskModelForm(instance=task)
    
    return render(request, "task/edit_task.html", context={'form': form, 'task_id': task_id})

@login_required
def task_edit_success(request):
    return render(request, "task/task_edit_success.html")
