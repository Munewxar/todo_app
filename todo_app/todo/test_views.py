from django.test import TestCase

from todo.models import Task
from todo.forms import TaskForm

from django.contrib.auth.models import User


class ViewsTestCase(TestCase):
    TEST_USER1_USERNAME = "test1"
    TEST_USER1_PASSWORD = "test1"

    def setUp(self):
        self.test_user1 = User.objects.create_user(
            username=self.TEST_USER1_USERNAME,
            email="test1@email.com",
            password=self.TEST_USER1_PASSWORD,
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
            owner_id=self.test_user2.id,
        )

        self.tasks_for_user1 = [task1, task2]
        self.tasks_for_user2 = [task3]

    def test_call_tasks_deny_anonymous(self):
        response = self.client.get("/todo/tasks/", follow=True)
        self.assertEqual(response.status_code, 404)

    def test_call_new_task_deny_anonymous(self):
        response = self.client.get("/todo/new_task/", follow=True)
        self.assertEqual(response.status_code, 404)

    def test_call_complete_task_deny_anonymous(self):
        response = self.client.get("/todo/complete_task/1/", follow=True)
        self.assertEqual(response.status_code, 404)

    def test_delete_task_deny_anonymous(self):
        response = self.client.get("/todo/delete_task/1/", follow=True)
        self.assertEqual(response.status_code, 404)

    def test_call_index_success(self):
        response = self.client.get("/todo/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/index.html")

    def test_call_tasks_success(self):
        self.client.login(
            username=self.TEST_USER1_USERNAME, password=self.TEST_USER1_PASSWORD
        )

        response = self.client.get("/todo/tasks/")
        tasks_by_day = self._get_tasks_by_day()

        self.assertEquals(response.status_code, 200)
        self.assertListEqual(
            list(response.context["tasks_by_day"].keys()),
            list(tasks_by_day.keys()),
        )

    def test_call_new_task_returns_empty_form_when_request_method_get(self):
        self.client.login(
            username=self.TEST_USER1_USERNAME, password=self.TEST_USER1_PASSWORD
        )

        response = self.client.get("/todo/new_task/")

        self.assertEquals(response.status_code, 200)
        self.assertTrue(isinstance(response.context["form"], TaskForm))

    def test_call_new_task_creates_task_when_method_post_and_form_valid(
        self,
    ):
        self.client.login(
            username=self.TEST_USER1_USERNAME, password=self.TEST_USER1_PASSWORD
        )

        task_data = {"task_text": "test task creation", "day_of_the_week": Task.MONDAY}
        response = self.client.post("/todo/new_task/", task_data)

        dne = False
        try:
            Task.objects.get(task_text=task_data["task_text"])
        except Task.DoesNotExist:
            dne = True

        self.assertFalse(dne)
        self.assertRedirects(response, "/todo/tasks/")

    def test_call_new_task_fails_when_form_invalid(self):
        self.client.login(
            username=self.TEST_USER1_USERNAME, password=self.TEST_USER1_PASSWORD
        )

        response = self.client.post("/todo/new_task/", {})

        self.assertFormError(response, "form", "task_text", "This field is required.")
        self.assertFormError(
            response, "form", "day_of_the_week", "This field is required."
        )

    def test_call_complete_task_completes_task(self):
        self.client.login(
            username=self.TEST_USER1_USERNAME, password=self.TEST_USER1_PASSWORD
        )

        task = self.tasks_for_user1[0]
        response = self.client.get(f"/todo/complete_task/{task.id}/")

        task_after_completion = Task.objects.get(pk=task.id)
        self.assertEquals(task_after_completion.status, Task.COMPLETED)
        self.assertRedirects(response, "/todo/tasks/")

    def test_call_delete_task_deletes_task(self):
        self.client.login(
            username=self.TEST_USER1_USERNAME, password=self.TEST_USER1_PASSWORD
        )

        task = self.tasks_for_user1[0]
        response = self.client.get(f"/todo/delete_task/{task.id}/")

        dne = False
        try:
            Task.objects.get(pk=task.id)
        except Task.DoesNotExist:
            dne = True

        self.assertTrue(dne)
        self.assertRedirects(response, "/todo/tasks/")

    # TODO: refactor reuse test_services functions
    def _get_tasks_by_day(self):
        days_of_the_week = Task.DAYS_OF_THE_WEEK
        current_day_index = Task.current_day_index

        sorted_tasks_by_day = {}
        i = current_day_index
        counter = 0

        tasks_by_day = self._distribute_tasks_by_days(self.tasks_for_user1)

        while counter < len(days_of_the_week):
            if i == len(days_of_the_week):
                i = 0

            day = days_of_the_week[i]
            if day in tasks_by_day.keys():
                sorted_tasks_by_day[day] = tasks_by_day[day]

            i += 1
            counter += 1

        return sorted_tasks_by_day

    def _distribute_tasks_by_days(self, tasks):
        tasks_by_day = {}

        for task in tasks:
            if task.day_of_the_week in tasks_by_day:
                tasks_by_day[task.day_of_the_week].append(task)
            else:
                tasks_by_day[task.day_of_the_week] = []
                tasks_by_day[task.day_of_the_week].append(task)

        return tasks_by_day
