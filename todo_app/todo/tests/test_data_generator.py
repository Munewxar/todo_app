import random

from todo.models import Task

from django.contrib.auth.models import User


class TestDataGenerator:
    USER1_USERNAME = "test1"
    USER1_PASSWORD = "test1"

    USER2_USERNAME = "test2"
    USER2_PASSWORD = "test2"

    USERS_CREDENTIALS = {
        USER1_USERNAME: {
            "username": USER1_USERNAME,
            "password": USER1_PASSWORD,
        },
        USER2_USERNAME: {
            "username": USER2_USERNAME,
            "password": USER2_PASSWORD,
        }
    }

    def __init__(self):
        self._user1 = User.objects.create_user(
            username=self.USER1_USERNAME,
            email="test1@email.com",
            password=self.USER1_PASSWORD,
        )

        self._user2 = User.objects.create_user(
            username=self.USER2_USERNAME,
            email="test2@email.com",
            password=self.USER2_PASSWORD,
        )

        self._tasks_for_user1 = self._generate_tasks(7, self._user1)
        self._tasks_for_user2 = self._generate_tasks(5, self._user2)

    def get_user1(self):
        return self._user1

    def get_user2(self):
        return self._user2

    def get_tasks_for_user1(self):
        return self._tasks_for_user1

    def get_tasks_for_user2(self):
        return self._tasks_for_user2

    def get_tasks_distributed_by_day(self, tasks):
        tasks_by_day = {}

        for task in tasks:
            if task.day_of_the_week in tasks_by_day:
                tasks_by_day[task.day_of_the_week].append(task)
            else:
                tasks_by_day[task.day_of_the_week] = []
                tasks_by_day[task.day_of_the_week].append(task)

        return tasks_by_day

    def get_tasks_sorted_by_day_of_the_week(self, tasks):
        tasks_by_day = self.get_tasks_distributed_by_day(tasks)

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

    def get_user_credentials(self, username):
        if username in self.USERS_CREDENTIALS:
            return self.USERS_CREDENTIALS[username]
        else: 
            raise ValueError(f"No such user: \"{username}\"")

    def _generate_user(self, username, email, password):
        return User.objects.create_user(
            username=username, email=email, password=password
        )

    def _generate_tasks(self, amount, user):
        tasks = []
        for i in range(amount):
            task = Task.objects.create(
                day_of_the_week=Task.DAYS_OF_THE_WEEK[random.randint(0, 6)],
                status=Task.NOT_COMPLETED,
                task_text=f"Test {i + 1}",
                owner_id=user.id,
            )
            tasks.append(task)

        return tasks
