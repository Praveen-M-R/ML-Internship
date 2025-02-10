# Celery Task Scheduling Guide

## Setting Up Celery in Django and Flask

### 1. Install Required Packages
Before setting up Celery, install the necessary dependencies using:
```sh
pip install celery redis django-celery-beat
```

## Setting Up Celery in a Django Application

### 2. Configure Celery in Django

#### **Django Project Structure**
```
my_project/
    my_project/
        __init__.py
        celery.py
        settings.py
    my_app/
        tasks.py
```

#### **Configure Celery in Django (`my_project/celery.py`)**
```python
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")

app = Celery("my_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
```

#### **Add Celery Configuration in `settings.py`**
```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
```

#### **Creating a Celery Task in Django (`my_app/tasks.py`)**
```python
from celery import shared_task

@shared_task
def add(x, y):
    return x + y
```

### 3. Running Celery in Django
Start the Celery worker:
```sh
celery -A my_project worker --loglevel=info
```

## Setting Up Celery in a Flask Application

### 4. Configure Celery in Flask

#### **Create a Flask App with Celery Integration**
```python
from flask import Flask
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0'
    )
    celery.conf.update(app.config)
    return celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)
celery = make_celery(app)

@app.route('/')
def home():
    return 'Flask App with Celery'

if __name__ == "__main__":
    app.run(debug=True)
```

#### **Creating a Celery Task in Flask**
```python
@celery.task
def add(x, y):
    return x + y
```

### 5. Running Celery in Flask
Start the Celery worker:
```sh
celery -A your_flask_app.celery worker --loglevel=info
```

## Setting Up Celery Beat for Periodic Tasks
To schedule periodic tasks, install Celery Beat:
```sh
pip install celery-beat
```

### 6. Configure Celery Beat in Django and Flask
#### **Django (`settings.py`)**
```python
INSTALLED_APPS += ['django_celery_beat']
```
Run migrations and create database tables:
```sh
python manage.py migrate django_celery_beat
```

#### **Flask (`tasks.py`)**
```python
from celery.schedules import crontab

app.conf.beat_schedule = {
    'run-every-1-minute': {
        'task': 'tasks.scheduled_task',
        'schedule': 60.0,  # Run every 60 seconds
    },
}
app.conf.timezone = 'UTC'
```

### 7. Starting Celery Beat
Create the schedule database file if it does not exist:
```sh
touch celerybeat-schedule.db
```
Start Celery Beat:
```sh
celery -A my_project beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

