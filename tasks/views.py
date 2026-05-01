from django.shortcuts import render, redirect
from .models import Task
from datetime import date
from supabase import create_client
from django.conf import settings
import uuid

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


today = date.today()

def home(request):
    if request.method == "POST":
        title = request.POST.get("title")
        due_date = request.POST.get("due_date")
        description = request.POST.get("description")
        image_file = request.FILES.get("image")
        image_url = upload_to_supabase(image_file) if image_file else None

        if title:
            Task.objects.create(
                title=title,
                description=description,
                image_url=image_url,
                due_date=due_date if due_date else None
            )
        return redirect("/")


    tasks = Task.objects.all()
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
        task.description = request.POST.get("description")
        task.due_date = due_date if due_date else None

        image_file = request.FILES.get("image")
        if image_file:
            task.image_url = upload_to_supabase(image_file)

        task.save()
        return redirect("/")

    return render(request, "tasks/edit_task.html", {"task": task})

def recover_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = False
    task.save()
    return redirect("/?filter=active")

def complete_all(request):
    Task.objects.filter(completed=False).update(completed=True)
    return redirect("/?filter=completed")