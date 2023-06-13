from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Task
from .forms import TaskForm


# Create your views here.
def index(request):
    return render(request, "todo/index.html")


# TODO: refactor
def tasks(request):
    tasks = Task.objects.filter(owner=request.user.id, status=Task.NOT_COMPLETED)

    tasks_by_day = {}
    for task in tasks:
        if task.day_of_the_week in tasks_by_day:
            tasks_by_day[task.day_of_the_week].append(task)
        else:
            tasks_by_day[task.day_of_the_week] = []
            tasks_by_day[task.day_of_the_week].append(task)

    days_of_the_week = Task.DAYS_OF_THE_WEEK
    current_day_index = Task.current_day_index

    sorted_tasks_by_day = {}
    i = current_day_index
    counter = 0
    while counter < len(days_of_the_week):
        if i == len(days_of_the_week):
            i = 0

        day = days_of_the_week[i]
        if day in tasks_by_day.keys():
            sorted_tasks_by_day[day] = tasks_by_day[day]

        i += 1
        counter += 1

    return render(request, "todo/tasks.html", {"tasks_by_day": sorted_tasks_by_day})


def new_task(request):
    if request.method != "POST":
        form = TaskForm()
    else:
        form = TaskForm(data=request.POST)

        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.status = Task.NOT_COMPLETED
            new_task.save()

            return redirect("todo:tasks")
        
    context = {"form" : form}
    return render(request, "todo/new_task.html", context)


def login(request):
    pass
