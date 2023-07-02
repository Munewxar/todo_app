# 📜 ToDo App

**ToDo App** helps you to manage your life easier. Create tasks, complete them and then delete! You don't need to keep in mind all of your tasks for the rest of the week.

## Screenshots

Home page:
![Home page](https://github.com/Munewxar/todo_app/blob/master/screenshots/index_page.png)

Tasks page:
![Tasks page](https://github.com/Munewxar/todo_app/blob/master/screenshots/tasks_page.png)

Task creation page:
![Task creation page](https://github.com/Munewxar/todo_app/blob/master/screenshots/new_task_page.png)

## Setup

1. Clone project to your machine

```
$ git clone https://github.com/Munewxar/todo_app.git

```

2. Create virtual environment and install dependencies

```

$ python -m venv /path/to/new/virtual/environment
$ pip install -r requirements.txt

```

3. Migrate data

```

$ python manage.py makemigrations
$ python manage.py migrate

```

4. Create super user

```

$ python manage.py createsuperuser

```

5. Run server

```

$ python manage.py runserver

```

6. Open web browser and go to [http://localhost:8000/todo/](http://localhost:8000/todo/)

## Technologies

**Python** - 3.11.2
**Django** - 4.2
