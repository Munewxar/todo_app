from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import TaskForm

import services


def index(request):
    return render(request, "todo/index.html")


@login_required
def tasks(request):
    tasks_by_day = services.retrieve_tasks_sorted_by_day_for_user(request.user.id)
    return render(request, "todo/tasks.html", {"tasks_by_day": tasks_by_day})


@login_required
def new_task(request):
    if request.method != "POST":
        form = TaskForm()
    else:
        new_task = services.create_new_task(request.POST, request.user.id)
        if new_task:
            return redirect("todo:tasks")
        
    context = {"form" : form}
    return render(request, "todo/new_task.html", context)


@login_required
def complete_task(request, task_id):
    services.complete_task(task_id)
    return redirect("todo:tasks")


@login_required
def delete_task(request, task_id):
    services.delete_task(task_id)
    return redirect("todo:tasks")
