from django.shortcuts import render, redirect
from .models import Task
from datetime import date
from supabase import create_client
from django.conf import settings
import uuid
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def upload_to_supabase(file):
    filename = f"{uuid.uuid4()}_{file.name}"

    file_bytes = file.read() 

    response = supabase.storage.from_("task-images").upload(
        path=filename,
        file=file_bytes,
        file_options={"content-type": file.content_type}
    )

    print("UPLOAD RESPONSE:", response)

    public_url = supabase.storage.from_("task-images").get_public_url(filename)

    return public_url


def task_json(request, task_id):
    task = Task.objects.get(id=task_id)

    return JsonResponse({
        "title": task.title,
        "description": task.description or "",
        "due_date": (
            task.due_date.strftime("%Y-%m-%d")
            if task.due_date else ""
        ),
        "image_url": task.image_url or "",
        "color": task.color,
    })

today = date.today()

#view to display tasks and handle task creation
@login_required(login_url='/login/')
def home(request):
    if request.method == "POST":
        title = request.POST.get("title")
        due_date = request.POST.get("due_date")
        description = request.POST.get("description")
        image_file = request.FILES.get("image")
        image_url = upload_to_supabase(image_file) if image_file else None

        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                description=description,
                image_url=image_url,
                due_date=due_date if due_date else None,
                color=request.POST.get("color", "white")
            )
        return redirect("/")


    tasks = Task.objects.filter(user=request.user)
    filter_type = request.GET.get("filter", "active")

    
    if filter_type == "completed":
        tasks = Task.objects.filter(completed=True)
    else:
        tasks = Task.objects.filter(completed=False)
    
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

#view to mark a task as complete
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect("/")

#view to delete a task
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect("/")

#view to edit a task
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":

        task.title = request.POST.get("title")
        due_date = request.POST.get("due_date")
        task.description = request.POST.get("description")
        task.due_date = due_date if due_date else None
        task.color = request.POST.get("color", "white")

        if request.POST.get("remove_image"):
            task.image_url = ""

        image_file = request.FILES.get("image")
        if image_file:
            task.image_url = upload_to_supabase(image_file)

        task.save()
        return redirect("/")

    return render(request, "tasks/edit_task.html", {"task": task})

#view to recover a completed task
@login_required
def recover_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = False
    task.save()
    return redirect("/?filter=active")

#view to mark all tasks as complete
@login_required
def complete_all(request):
    Task.objects.filter(user=request.user, completed=False).update(completed=True)
    return redirect("/?filter=completed")

#view to search for tasks
@login_required
def search_tasks(request):
    query = request.GET.get("q", "")
    tasks = Task.objects.filter(user=request.user, title__icontains=query)
    return render(request, "tasks/home.html", {"tasks": tasks, "query": query})

#view to clear all completed tasks
@login_required
def clear_completed(request):
    Task.objects.filter(user=request.user, completed=True).delete()
    return redirect("/?filter=active")

#view to return home
@login_required
def return_home(request):
    return redirect("/")