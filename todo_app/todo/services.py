from django.shortcuts import get_object_or_404

from .models import Task
from .forms import TaskForm


def retrieve_tasks_sorted_by_day_for_user(user_id):
    tasks = _get_tasks_by_user_id(user_id)
    tasks_by_day = _distribute_tasks_by_days(tasks)
    sorted_tasks_by_day = _sort_tasks_by_day_based_on_current_day_of_the_week(
        tasks_by_day
    )

    return sorted_tasks_by_day


def create_new_task(task_data, user_id):
    form = TaskForm(task_data)

    if form.is_valid():
        new_task = form.save(commit=False)
        new_task.owner = user_id
        new_task.status = Task.NOT_COMPLETED
        new_task.save()

        return new_task
    
    return None


def complete_task(task_id):
    task = _get_task_by_id(task_id)
    task.status = Task.COMPLETED
    task.save()


def delete_task(task_id):
    task = _get_task_by_id(task_id)
    task.delete()


def _get_task_by_id(task_id):
    return get_object_or_404(Task, id=task_id)


def _get_tasks_by_user_id(user_id):
    tasks = Task.objects.filter(owner=user_id)
    return tasks


def _distribute_tasks_by_days(tasks):
    tasks_by_day = {}

    for task in tasks:
        if task.day_of_the_week in tasks_by_day:
            tasks_by_day[task.day_of_the_week].append(task)
        else:
            tasks_by_day[task.day_of_the_week] = []
            tasks_by_day[task.day_of_the_week].append(task)

    return tasks_by_day


def _sort_tasks_by_day_based_on_current_day_of_the_week(tasks_by_day):
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

    return sorted_tasks_by_day
