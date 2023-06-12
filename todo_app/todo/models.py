from django.db import models
from django.conf import settings

from datetime import datetime


# Create your models here.
class Task(models.Model):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

    DAYS_OF_THE_WEEK = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY]

    DAY_OF_THE_WEEK_CHOICES = [
        (MONDAY, "Monday"),
        (TUESDAY, "Tuesday"),
        (WEDNESDAY, "Wednesday"),
        (THURSDAY, "Thursday"),
        (FRIDAY, "Friday"),
        (SATURDAY, "Saturday"),
        (SUNDAY, "Sunday"),
    ]

    NOT_COMPLETED = "NC"
    COMPLETED = "C"

    STATUS_CHOICES = [
        (NOT_COMPLETED, "Not completed"),
        (COMPLETED, "Completed"),
    ]

    dt = datetime.now()
    current_day_index = dt.weekday()
    default_day = DAYS_OF_THE_WEEK[current_day_index]

    day_of_the_week = models.CharField(
        max_length=10, choices=DAY_OF_THE_WEEK_CHOICES, default=default_day
    )

    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=NOT_COMPLETED
    )

    task_text = models.CharField(max_length=200)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        if len(self.task_text) > 50:
            return f"{self.task_text[:50]}..."

        return self.task_text
