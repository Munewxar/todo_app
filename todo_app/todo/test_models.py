from django.test import TestCase
from todo.models import Task

from django.contrib.auth.models import User

from datetime import datetime


class TaskTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            username="test1",
            email="test@email.com",
            password="test1"
        )

        Task.objects.create(
            task_text="Test default",
            owner_id=test_user.id
        )

        Task.objects.create(
            day_of_the_week=Task.MONDAY,
            status=Task.NOT_COMPLETED,
            task_text="Test 1",
            owner_id=test_user.id
        )


    def test_task_coorectly_creates_with_default_fields(self):
        test_task = Task.objects.get(task_text="Test default")

        dt = datetime.now()
        current_day_index = dt.weekday()
        current_day_of_the_week = Task.DAYS_OF_THE_WEEK[current_day_index]

        self.assertEqual(test_task.day_of_the_week, current_day_of_the_week)
        self.assertEqual(test_task.status, Task.NOT_COMPLETED)


    def test_task_creates_correctly(self):
        test_task = Task.objects.get(task_text="Test 1")

        self.assertEqual(test_task.day_of_the_week, Task.MONDAY)
        self.assertEqual(test_task.status, Task.NOT_COMPLETED)
        self.assertEqual(test_task.task_text, "Test 1")
        self.assertEqual(test_task.owner.username, "test1")