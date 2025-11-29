

# Create your views here.
from django.shortcuts import render, redirect ,get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Task

def home(request):
    if request.method == "POST":
        title = request.POST.get("title")
        reminder_time = request.POST.get("reminder_time")  # get from form

        if title:
            if reminder_time:
                # convert string to datetime
                from datetime import datetime
                reminder_dt = datetime.fromisoformat(reminder_time)
            else:
                reminder_dt = timezone.now()  # default current time

            Task.objects.create(
                title=title,
                reminder_time=reminder_dt
            )
        return redirect("home")

    tasks = Task.objects.order_by('-created_at')
    return render(request, "tasks/home.html", {"tasks": tasks, "now": timezone.now()})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("home")
    return render(request, "tasks/confirm_delete.html", {"task": task})

def check_reminders(request):
    now = timezone.now()

    due_tasks = Task.objects.filter(
        reminder_time__lte=now,
        reminder_time__isnull=False
    )

    reminder_list = [{"title": t.title} for t in due_tasks]

    # Clear reminder so popup doesn't repeat
    due_tasks.update(reminder_time=None)

    return JsonResponse({"reminders": reminder_list})