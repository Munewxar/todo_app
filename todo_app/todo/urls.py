from django.urls import path

from . import views

app_name = "todo"
urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/", views.tasks, name="tasks"),
    path("new_task/", views.new_task, name="new_task"),
    path("complete_task/<int:task_id>/", views.complete_task, name="complete_task"),
    path("delete_task/<int:task_id>/", views.delete_task, name="delete_task"),
]
