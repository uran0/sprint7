from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django .utils.timezone import now
from .models import Status, Task, Tag, Priority
from account.models import User
from .forms import TaskForm
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
def delete_task(request,task_name):
    try:
        user=User.objects.get(username=request.user.username)
        task=Task.objects.get(name=task_name, user=user)
        task.delete()
        return redirect("task_list")
    except Task.DoesNotExist:
        return redirect("task_list")


@login_required
def edit_task(request, task_name):
    try:
        if request.method=="POST":
            form=TaskForm(user=request.user.username, data=request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = User.objects.get(username=request.user.username)
                task = Task.objects.get(user=user, name=task_name)                
                task.user = user
                task.name = data["name"]
                task.description = data["description"] if data["description"]!="" else "-sin información-"
                task.expire_date = data["expire_date"]
                task.status = Status.objects.get(id=data["status"])
                task.tag = Tag.objects.get(id=data["tag"]) 
                task.save()
                return redirect("/home")
        else:
            initial_data = {
                'name': task.name,
                'description': task.description,
                'expire_date': task.expire_date,
                'status': task.status.id,
                'tag': task.tag.id,
            }
            form = TaskForm(user=request.user.username, initial=initial_data)
    
    except Task.DoesNotExist:
        return redirect("task_list")
    
    return render(request, "new_task.html", context={'form': form, 'task_name': task_name})