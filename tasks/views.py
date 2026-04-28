from django.shortcuts import render, redirect
from .models import Task
from datetime import date


today = date.today()

def home(request):
    if request.method == "POST":
        title = request.POST.get("title")
        due_date = request.POST.get("due_date")

        if title:
            Task.objects.create(
                title=title,
                due_date=due_date if due_date else None
            )
        return redirect("/")


    tasks = Task.objects.all()
    filter_type = request.GET.get("filter")

    
    if filter_type == "active":
        tasks = tasks.filter(completed=False)
    elif filter_type == "completed":
        tasks = tasks.filter(completed=True)

    
    tasks = sorted(
        tasks,
        key=lambda task: (
            task.completed,
            0 if task.due_date and task.due_date < today else
            1 if task.due_date == today else
            2 if task.due_date else
            3,
            task.due_date or today
        )
    )

    return render(request, "tasks/home.html", {
        "tasks": tasks,
        "today": today,
        "current_filter": filter_type
    })


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