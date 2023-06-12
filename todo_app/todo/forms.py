from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["day_of_the_week", "task_text", "status"]
        labels = {
            "day_of_the_week": "Day",
            "task_text": "Task",
            "status": "Status",
        }