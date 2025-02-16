# Setting Up and Managing Periodic Tasks in Django (Using django-celery-beat)

## 📌 Prerequisites

Ensure you have the following installed and configured:
- Django
- Celery
- Redis (as a message broker)
- django-celery-beat

If you haven't installed `django-celery-beat`, install it using:

```bash
pip install django-celery-beat
```

Then, **migrate the database**:

```bash
python manage.py migrate django_celery_beat
```

## ✅ Step 1: Check Existing Periodic Tasks

Run the Django shell:

```bash
python manage.py shell
```

Then, check if there are any existing periodic tasks:

```python
from django_celery_beat.models import PeriodicTask
print(PeriodicTask.objects.values("name", "task", "enabled"))
```

### Expected Output:

- If tasks exist:
  ```python
  <QuerySet [{'name': 'Check Missing Pings', 'task': 'checks.tasks.check_missing_pings', 'enabled': True}]>
  ```
- If no tasks exist, the output will be an empty QuerySet (`[]`).

## ❌ Step 2: Delete Existing Periodic Tasks (Optional)

If an old task is not working properly or needs to be recreated, delete all periodic tasks:

```python
from django_celery_beat.models import PeriodicTask, IntervalSchedule
PeriodicTask.objects.all().delete()
IntervalSchedule.objects.all().delete()
```

## 🔄 Step 3: Create a New Periodic Task

### 3.1 Define the Celery Task
Ensure your Celery task exists in `checks/tasks.py`:

```python
from celery import shared_task

@shared_task
def check_missing_pings():
    print("Checking for missing pings...")
```

### 3.2 Create the Task in django-celery-beat

Now, create the periodic task in the Django shell:

```python
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from datetime import timedelta
import json

# Create an interval schedule (every 10 seconds)
schedule, created = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.SECONDS
)

# Create the periodic task
PeriodicTask.objects.create(
    interval=schedule,
    name="Check Missing Pings",
    task="checks.tasks.check_missing_pings",
    args=json.dumps([]),  # Empty args
    enabled=True
)
```

Verify the task was created:

```python
print(PeriodicTask.objects.values("name", "task", "enabled"))
```

## 🚀 Step 4: Start Celery and Celery Beat

After setting up the task, restart Celery and Celery Beat:

### 4.1 Start Redis (if not running)

```bash
redis-server &
```

### 4.2 Start Celery Worker

```bash
celery -A healthcheck worker --loglevel=info
```

### 4.3 Start Celery Beat

```bash
celery -A healthcheck beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## 🛠 Step 5: Verify Task Execution

If everything is working correctly, Celery Beat should log:

```bash
[2025-02-16 15:00:12,591: INFO/MainProcess] Scheduler: Sending due task check_missing_pings
```

And the Celery Worker should log:

```bash
[2025-02-16 15:00:12,600: INFO/ForkPoolWorker-1] Task checks.tasks.check_missing_pings succeeded in 0.007s
```

## 🔍 Debugging Issues

### 1️⃣ If the task doesn't run, check if Celery Beat is scheduling tasks:
```python
print(PeriodicTask.objects.values("name", "task", "enabled"))
```

### 2️⃣ If Celery Beat doesn't start, reset the schedule:
```bash
rm celerybeat-schedule
celery -A healthcheck beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### 3️⃣ If the worker isn't processing tasks, restart it:
```bash
pkill -9 -f "celery"
celery -A healthcheck worker --loglevel=info
```

---

Now you have a **fully working Celery periodic task system** in Django! 🚀🎉

