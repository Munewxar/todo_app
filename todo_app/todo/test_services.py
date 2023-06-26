from django.test import TestCase
from todo.models import Task
from todo.forms import TaskForm

from django.contrib.auth.models import User

import todo.services as services


class ServicesTestCase(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(
            username="test1", email="test1@email.com", password="test1"
        )

        self.test_user2 = User.objects.create_user(
            username="test2", email="test2@email.com", password="test2"
        )

        task1 = Task.objects.create(
            day_of_the_week=Task.MONDAY,
            status=Task.NOT_COMPLETED,
            task_text="Test 1",
            owner_id=self.test_user1.id,
        )

        task2 = Task.objects.create(
            day_of_the_week=Task.FRIDAY,
            status=Task.NOT_COMPLETED,
            task_text="Test 2",
            owner_id=self.test_user1.id,
        )

        task3 = Task.objects.create(
            day_of_the_week=Task.TUESDAY,
            status=Task.NOT_COMPLETED,
            task_text="Test 3",
            owner_id=self.test_user1.id,
        )

        task4 = Task.objects.create(
            day_of_the_week=Task.FRIDAY,
            status=Task.NOT_COMPLETED,
            task_text="Test 4",
            owner_id=self.test_user1.id,
        )

        task5 = Task.objects.create(
            day_of_the_week=Task.THURSDAY,
            status=Task.NOT_COMPLETED,
            task_text="Test 5",
            owner_id=self.test_user2.id,
        )

        self.tasks_for_user1 = [task1, task2, task3, task4]
        self.tasks_for_user2 = [task5]

    def test_get_task_by_id_returns_valid_task(self):
        expected_task = self.tasks_for_user1[0]
        actual_task = services._get_task_by_id(expected_task.id)

        self.assertEqual(actual_task, expected_task)

    def test_get_tasks_by_user_id_returns_valid_tasks(self):
        expected_tasks = self.tasks_for_user1
        actual_tasks = services._get_tasks_by_user_id(self.test_user1.id)

        self.assertCountEqual(actual_tasks, expected_tasks)

    def test_delete_task_by_id_deletes_valid_task(self):
        task_to_delete_id = self.tasks_for_user2[0].id
        services.delete_task_by_id(task_to_delete_id)

        dne_exeption_raised = False
        try:
            Task.objects.get(id=task_to_delete_id)
        except Task.DoesNotExist:
            dne_exeption_raised = True

        self.assertTrue(dne_exeption_raised)

    def test_complete_task_by_id_changes_task_status_to_completed(self):
        test_task_id = self.tasks_for_user1[0].id
        services.complete_task_by_id(test_task_id)

        test_task_after_completion = Task.objects.get(id=test_task_id)
        self.assertEquals(test_task_after_completion.status, Task.COMPLETED)

    def test_create_new_task_based_on_form_correctly_creates_task(self):
        day_of_the_week = Task.MONDAY
        task_text = "testing task creation"
        task_data = {"day_of_the_week": day_of_the_week, "task_text": task_text}

        dne_exception_raised = False
        try:
            Task.objects.get(task_text=task_text)
        except Task.DoesNotExist:
            dne_exception_raised = True

        self.assertTrue(dne_exception_raised)

        services.create_new_task_based_on_form(task_data, self.test_user1)

        task = Task.objects.get(task_text=task_text)
        self.assertEqual(task.task_text, task_text)
        self.assertEqual(task.day_of_the_week, day_of_the_week)

    def test_distribute_tasks_by_days(self):
        expected_tasks_by_day = self._get_tasks_distributed_by_day()
        actual_tasks_by_day = services._distribute_tasks_by_days(self.tasks_for_user1)

        self.assertDictEqual(actual_tasks_by_day, expected_tasks_by_day)

    def test_sort_tasks_by_day_based_on_current_day_of_the_week(self):
        tasks_by_day = self._get_tasks_distributed_by_day()
        expected_sorted_tasks_by_day = self._get_tasks_sorted_by_day_of_the_week(
            tasks_by_day
        )
        actual_sorted_tasks_by_day = (
            services._sort_tasks_by_day_based_on_current_day_of_the_week(tasks_by_day)
        )

        self.assertListEqual(
            list(actual_sorted_tasks_by_day.keys()),
            list(expected_sorted_tasks_by_day.keys()),
        )

    def test_retrieve_tasks_sorted_by_day_for_user(self):
        tasks_by_day = self._get_tasks_distributed_by_day()
        expected_sorted_tasks_by_day = self._get_tasks_sorted_by_day_of_the_week(
            tasks_by_day
        )
        actual_tasks_by_day = services.retrieve_tasks_sorted_by_day_for_user(
            self.test_user1.id
        )

        self.assertDictEqual(actual_tasks_by_day, expected_sorted_tasks_by_day)

    def _get_tasks_distributed_by_day(self):
        tasks_by_day = {}

        for task in self.tasks_for_user1:
            if task.day_of_the_week in tasks_by_day:
                tasks_by_day[task.day_of_the_week].append(task)
            else:
                tasks_by_day[task.day_of_the_week] = []
                tasks_by_day[task.day_of_the_week].append(task)

        return tasks_by_day

    def _get_tasks_sorted_by_day_of_the_week(self, tasks_by_day):
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