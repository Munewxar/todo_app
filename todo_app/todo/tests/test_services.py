from django.test import TestCase

from todo.models import Task

from django.contrib.auth.models import User

import todo.services as services

from .test_data_generator import TestDataGenerator


class ServicesTestCase(TestCase):
    def setUp(self):
        self.test_data = TestDataGenerator()

    def test_get_task_by_id_returns_valid_task(self):
        tasks = self.test_data.get_tasks_for_user1()
        expected_task = tasks[0]

        actual_task = services._get_task_by_id(expected_task.id)
        self.assertEqual(actual_task, expected_task)

    def test_get_tasks_by_user_id_returns_valid_tasks(self):
        expected_tasks = self.test_data.get_tasks_for_user1()
        user = self.test_data.get_user1()

        actual_tasks = services._get_tasks_by_user_id(user.id)
        self.assertCountEqual(actual_tasks, expected_tasks)

    def test_delete_task_by_id_deletes_valid_task(self):
        tasks = self.test_data.get_tasks_for_user2()
        task_to_delete_id = tasks[0].id
        services.delete_task_by_id(task_to_delete_id)

        dne_exeption_raised = False
        try:
            Task.objects.get(id=task_to_delete_id)
        except Task.DoesNotExist:
            dne_exeption_raised = True

        self.assertTrue(dne_exeption_raised)

    def test_complete_task_by_id_changes_task_status_to_completed(self):
        tasks = self.test_data.get_tasks_for_user1()
        test_task_id = tasks[0].id
        services.complete_task_by_id(test_task_id)

        test_task_after_completion = Task.objects.get(id=test_task_id)
        self.assertEquals(test_task_after_completion.status, Task.COMPLETED)

    def test_create_new_task_based_on_form_correctly_creates_task(self):
        day_of_the_week = Task.MONDAY
        task_text = "testing task creation"
        task_data = {"day_of_the_week": day_of_the_week, "task_text": task_text}

        user = self.test_data.get_user1()
        services.create_new_task_based_on_form(task_data, user)

        task = Task.objects.get(task_text=task_text)
        self.assertEqual(task.task_text, task_text)
        self.assertEqual(task.day_of_the_week, day_of_the_week)

    def test_distribute_tasks_by_days(self):
        tasks = self.test_data.get_tasks_for_user1()
        expected_tasks_by_day = self.test_data.get_tasks_distributed_by_day(tasks)
        actual_tasks_by_day = services._distribute_tasks_by_days(tasks)

        self.assertDictEqual(actual_tasks_by_day, expected_tasks_by_day)

    def test_sort_tasks_by_day_based_on_current_day_of_the_week(self):
        tasks = self.test_data.get_tasks_for_user1()

        expected_sorted_tasks_by_day = (
            self.test_data.get_tasks_sorted_by_day_of_the_week(tasks)
        )

        tasks_by_day = self.test_data.get_tasks_distributed_by_day(tasks)
        actual_sorted_tasks_by_day = (
            services._sort_tasks_by_day_based_on_current_day_of_the_week(tasks_by_day)
        )

        self.assertListEqual(
            list(actual_sorted_tasks_by_day.keys()),
            list(expected_sorted_tasks_by_day.keys()),
        )

    def test_retrieve_tasks_sorted_by_day_for_user(self):
        tasks = self.test_data.get_tasks_for_user1()
        expected_sorted_tasks_by_day = (
            self.test_data.get_tasks_sorted_by_day_of_the_week(tasks)
        )

        user = self.test_data.get_user1()
        actual_tasks_by_day = services.retrieve_tasks_sorted_by_day_for_user(user.id)

        self.assertDictEqual(actual_tasks_by_day, expected_sorted_tasks_by_day)
