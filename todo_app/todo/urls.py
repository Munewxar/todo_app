from django.urls import path

from . import views

app_name = "todo"
urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/", views.tasks, name="tasks"),
    path("new_task/", views.new_task, name="new_task"),
]
