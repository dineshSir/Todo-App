from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TaskForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from django.db.models import Q, Count, Sum


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, "todo/register.html",)

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                tasks = Task.objects.filter(user=request.user)
                username = user.username.capitalize()
                return render(request, 'todo/task_list.html', {'username':username, 'tasks':tasks})
            else:
                messages.error(request, "Invalid Credentials")

    return render(request, 'todo/login.html',)

@login_required
def task_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    username = request.user.username.capitalize()
    if request.method == "GET": 
        status = request.GET.get('status', 'all')
        if status == 'all':
            tasks = Task.objects.filter(user=request.user)
        elif status == 'completed':
            tasks = Task.objects.filter(user=request.user, completed=True)
        else:
            tasks = Task.objects.filter(user=request.user, completed=False)
    else:
        tasks = Task.objects.filter(user=request.user)

    return render(request, 'todo/task_list.html', {'tasks':tasks, 'status_filter':status,'username':username})

@login_required
def logout_view(request):
    return redirect('login')

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            form.save()
            return redirect('task_list')
    return render(request, 'todo/add_task.html')

@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    return redirect('task_list')

@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        print(request.POST)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            form.save()
            return redirect('task_list')
    return render(request, 'todo/edit_task.html', {'task':task})

@login_required
def completed(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if task.completed:
        task.completed = False
    else:
        task.completed = True
    task.save()
    return redirect('task_list')

def test_view(request):
    data = Task.objects.values_list('title', 'description')
    print(data)
    return render(request, 'todo/test.html', {'data':data})
    
    
