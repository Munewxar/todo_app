from django.test import TestCase

from todo.models import Task
from todo.forms import TaskForm

from django.contrib.auth.models import User

from .test_data_generator import TestDataGenerator


class ViewsTestCase(TestCase):
    TEST_USER1_USERNAME = "test1"
    TEST_USER1_PASSWORD = "test1"

    INDEX_URL = "/todo/"
    TASKS_URL = "/todo/tasks/"
    NEW_TASK_URL = "/todo/new_task/"
    COMPLETE_TASK_URL = "/todo/complete_task/{}/"
    DELETE_TASK_URL = "/todo/delete_task/{}/"
    REDIRECT_AFTER_LOGIN_URL = "/users/login/?next="

    def setUp(self):
        self.test_data = TestDataGenerator()

    def test_call_tasks_deny_anonymous(self):
        response = self.client.get(self.TASKS_URL, follow=True)
        self.assertRedirects(
            response, f"{self.REDIRECT_AFTER_LOGIN_URL}{self.TASKS_URL}"
        )

    def test_call_new_task_deny_anonymous(self):
        response = self.client.get(self.NEW_TASK_URL, follow=True)
        self.assertRedirects(
            response, f"{self.REDIRECT_AFTER_LOGIN_URL}{self.NEW_TASK_URL}"
        )

    def test_call_complete_task_deny_anonymous(self):
        tasks = self.test_data.get_tasks_for_user1()
        task = tasks[0]
        formatted_complete_task_url = self.COMPLETE_TASK_URL.format(task.id)
        response = self.client.get(formatted_complete_task_url, follow=True)
        self.assertRedirects(
            response, f"{self.REDIRECT_AFTER_LOGIN_URL}{formatted_complete_task_url}"
        )

    def test_delete_task_deny_anonymous(self):
        tasks = self.test_data.get_tasks_for_user1()
        task = tasks[0]
        formatted_delete_task_url = self.DELETE_TASK_URL.format(task.id)
        response = self.client.get(formatted_delete_task_url, follow=True)
        self.assertRedirects(
            response, f"{self.REDIRECT_AFTER_LOGIN_URL}{formatted_delete_task_url}"
        )

    def test_call_index_success(self):
        response = self.client.get(self.INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/index.html")

    def test_call_tasks_success(self):
        self._login()

        response = self.client.get(self.TASKS_URL)
        tasks = self.test_data.get_tasks_for_user1()
        tasks_by_day = self.test_data.get_tasks_sorted_by_day_of_the_week(tasks)

        self.assertEquals(response.status_code, 200)
        self.assertListEqual(
            list(response.context["tasks_by_day"].keys()),
            list(tasks_by_day.keys()),
        )

    def test_call_new_task_returns_empty_form_when_request_method_get(self):
        self._login()

        response = self.client.get(self.NEW_TASK_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTrue(isinstance(response.context["form"], TaskForm))

    def test_call_new_task_success_when_method_post_and_form_valid(self):
        self._login()

        task_data = {"task_text": "test task creation", "day_of_the_week": Task.MONDAY}
        response = self.client.post(self.NEW_TASK_URL, task_data)

        dne = False
        try:
            Task.objects.get(task_text=task_data["task_text"])
        except Task.DoesNotExist:
            dne = True

        self.assertFalse(dne)
        self.assertRedirects(response, self.TASKS_URL)

    def test_call_new_task_fails_when_form_invalid(self):
        self._login()

        response = self.client.post(self.NEW_TASK_URL, {})

        self.assertFormError(response, "form", "task_text", "This field is required.")
        self.assertFormError(
            response, "form", "day_of_the_week", "This field is required."
        )

    def test_call_complete_task_completes_task(self):
        self._login()

        tasks = self.test_data.get_tasks_for_user1()
        task = tasks[0]
        formatted_complete_task_url = self.COMPLETE_TASK_URL.format(task.id)
        response = self.client.get(formatted_complete_task_url)

        task_after_completion = Task.objects.get(pk=task.id)
        self.assertEquals(task_after_completion.status, Task.COMPLETED)
        self.assertRedirects(response, self.TASKS_URL)

    def test_call_delete_task_deletes_task(self):
        self._login()

        tasks = self.test_data.get_tasks_for_user1()
        task = tasks[0]
        formatted_delete_task_url = self.DELETE_TASK_URL.format(task.id)
        response = self.client.get(formatted_delete_task_url)

        dne = False
        try:
            Task.objects.get(pk=task.id)
        except Task.DoesNotExist:
            dne = True

        self.assertTrue(dne)
        self.assertRedirects(response, self.TASKS_URL)

    def _login(self):
        user = self.test_data.get_user1()
        credentials = self.test_data.get_user_credentials(user.username)
        self.client.login(
            username=credentials["username"], password=credentials["password"]
        )
