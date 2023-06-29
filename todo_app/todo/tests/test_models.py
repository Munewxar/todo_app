from django.test import TestCase
from todo.models import Task

from django.contrib.auth.models import User

from datetime import datetime

from .test_data_generator import TestDataGenerator


class TaskTestCase(TestCase):
    def setUp(self):
        self.test_data = TestDataGenerator()

    def test_task_coorectly_creates_with_default_fields(self):
        user = self.test_data.get_user1()
        test_task = Task.objects.create(task_text="Test default", owner=user)

        dt = datetime.now()
        current_day_index = dt.weekday()
        current_day_of_the_week = Task.DAYS_OF_THE_WEEK[current_day_index]

        self.assertEqual(test_task.day_of_the_week, current_day_of_the_week)
        self.assertEqual(test_task.status, Task.NOT_COMPLETED)

    def test_task_creates_correctly(self):
        user = self.test_data.get_user1()
        task_text = "Test 1"
        test_task = Task.objects.create(
            day_of_the_week=Task.MONDAY,
            task_text=task_text,
            status=Task.NOT_COMPLETED,
            owner=user,
        )

        self.assertEqual(test_task.day_of_the_week, Task.MONDAY)
        self.assertEqual(test_task.status, Task.NOT_COMPLETED)
        self.assertEqual(test_task.task_text, task_text)
        self.assertEqual(test_task.owner.username, user.username)
