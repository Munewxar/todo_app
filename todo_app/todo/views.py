from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import TaskForm

from .services import (
    retrieve_tasks_sorted_by_day_for_user,
    create_new_task_based_on_form,
    complete_task_by_id,
    delete_task_by_id,
)


def index(request):
    return render(request, "todo/index.html")


@login_required
def tasks(request):
    tasks_by_day = retrieve_tasks_sorted_by_day_for_user(request.user.id)
    return render(request, "todo/tasks.html", {"tasks_by_day": tasks_by_day})


@login_required
def new_task(request):
    if request.method != "POST":
        form = TaskForm()
    else:
        form = create_new_task_based_on_form(request.POST, request.user)
        if form.is_valid():
            return redirect("todo:tasks")

    context = {"form": form}
    return render(request, "todo/new_task.html", context)


@login_required
def complete_task(request, task_id):
    complete_task_by_id(task_id)
    return redirect("todo:tasks")


@login_required
def delete_task(request, task_id):
    delete_task_by_id(task_id)
    return redirect("todo:tasks")
