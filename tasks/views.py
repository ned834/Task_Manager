from django.shortcuts import render, redirect
from .models import Task

def home(request):
    if request.method == "POST":
        title = request.POST.get("title")
        due_date = request.POST.get("due_date")
        if title:
            Task.objects.create(title=title, due_date=due_date if due_date else None)
        return redirect("/")

    tasks = Task.objects.all()
    return render(request, "tasks/home.html", {"tasks": tasks})

def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect("/")

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect("/")

def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == "POST":
        task.title = request.POST.get("title")
        due_date = request.POST.get("due_date")
        task.due_date = due_date if due_date else None
        task.save()
        return redirect("/")

    return render(request, "tasks/edit_task.html", {"task": task})