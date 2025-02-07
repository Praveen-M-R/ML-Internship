# 📌 Complete Guide to Setting Up & Configuring Celery

Celery is a **distributed task queue** that allows you to execute background jobs asynchronously. It is commonly used in **web applications, data processing, and automation tasks**.

---

## **1️⃣ What is Celery?**
✅ **Celery is an asynchronous task queue** that runs tasks in the background.  
✅ **It uses a message broker** (like **Redis** or **RabbitMQ**) to manage task execution.  
✅ **It supports scheduled tasks** using **Celery Beat**.  
✅ **It allows task retries, prioritization, and parallel execution.**  

---

## **2️⃣ Prerequisites**
### **🔹 Install Required Dependencies**
Before you begin, make sure you have Python installed (**version 3.6+ recommended**).

### **🔹 Install Celery & Redis**
```bash
pip install celery redis
```

If you're using **RabbitMQ** as the message broker, install Celery with:
```bash
pip install celery[librabbitmq]
```

### **🔹 Install Celery Beat (Optional, for Scheduled Tasks)**
```bash
pip install django-celery-beat
```

### **🔹 Install and Start Redis**
Celery requires a **message broker** to queue and distribute tasks.  
For Redis, install it using:
```bash
sudo apt update && sudo apt install redis
```
Start Redis:
```bash
redis-server
```
Check if Redis is running:
```bash
redis-cli ping
```
It should return:
```
PONG
```

---

## **3️⃣ Setting Up Celery in Your Project**
### **🔹 Create a Celery Instance**
Create a new file **`celery_app.py`**:
```python
from celery import Celery

app = Celery(
    "tasks",  
    broker="redis://localhost:6379/0",  
    backend="redis://localhost:6379/0"  
)

app.conf.update(
    result_expires=3600,  # Task results expire after 1 hour
    timezone="UTC",
)

@app.task
def add(x, y):
    return x + y
```

---

## **4️⃣ Running Celery**
### **🔹 Start Celery Worker**
To start Celery, run:
```bash
celery -A celery_app worker --loglevel=info
```
Output:
```
[2024-02-08 12:00:00,000: INFO/MainProcess] Connected to redis://localhost:6379/0
[2024-02-08 12:00:00,000: INFO/MainProcess] Worker: Ready.
```

### **🔹 Calling Tasks**
In a Python shell:
```python
from celery_app import add
result = add.delay(4, 6)
print(result.get())  # Output: 10
```

---

## **5️⃣ Configuring Celery in a Django Project**
### **🔹 Install Dependencies**
```bash
pip install django-celery-beat
```

### **🔹 Add Celery to `settings.py`**
```python
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
```

### **🔹 Create a `celery.py` File in Django**
Inside your Django app directory:
```python
from celery import Celery

app = Celery("myproject")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
```

### **🔹 Create a Celery Task**
Inside your Django app (e.g., `tasks.py`):
```python
from celery import shared_task

@shared_task
def add(x, y):
    return x + y
```

### **🔹 Run Celery with Django**
```bash
celery -A myproject worker --loglevel=info
```

---

## **6️⃣ Using Celery Beat for Scheduling**
Celery Beat **schedules tasks to run at fixed times** (like a cron job).  

### **🔹 Install Celery Beat**
```bash
pip install django-celery-beat
```

### **🔹 Start Celery Beat**
```bash
celery -A myproject beat --loglevel=info
```

### **🔹 Define a Periodic Task in `celery.py`**
```python
from celery.schedules import crontab

app.conf.beat_schedule = {
    "add-every-10-seconds": {
        "task": "myapp.tasks.add",
        "schedule": 10.0,  # Runs every 10 seconds
        "args": (5, 10),
    },
}
```

---

## **7️⃣ Handling Common Issues**
### **🛠 Celery Not Connecting to Redis**
- Ensure Redis is running:
  ```bash
  redis-cli ping
  ```
- Restart Redis if needed:
  ```bash
  sudo systemctl restart redis
  ```

### **🛠 Task Not Executing**
- Check if the worker is running:
  ```bash
  celery -A celery_app status
  ```
- Restart the worker:
  ```bash
  celery -A celery_app worker --loglevel=info
  ```

### **🛠 Celery Beat Schedule Not Running**
- Ensure `celerybeat-schedule.db` exists or recreate it:
  ```bash
  rm celerybeat-schedule.db
  touch celerybeat-schedule.db
  ```

---

## **8️⃣ Running Celery in Production**
### **🔹 Using Supervisor to Keep Celery Running**
Create a **Supervisor** config (`/etc/supervisor/conf.d/celery.conf`):
```ini
[program:celery]
command=celery -A myproject worker --loglevel=info
directory=/path/to/project
autostart=true
autorestart=true
stderr_logfile=/var/log/celery.err.log
stdout_logfile=/var/log/celery.out.log
```

### **🔹 Restart Supervisor**
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start celery
```

---

## **9️⃣ Summary**
| **Step** | **Command** |
|----------|------------|
| Install Celery | `pip install celery redis` |
| Install Celery Beat | `pip install django-celery-beat` |
| Start Redis | `redis-server` |
| Start Celery Worker | `celery -A celery_app worker --loglevel=info` |
| Start Celery Beat | `celery -A celery_app beat --loglevel=info` |
| Call a Task | `task_name.delay(args)` |

---

## **🎯 Final Thoughts**
✅ **Celery is perfect for background tasks, scheduling, and distributed processing.**  
✅ **With Celery Beat, you can schedule periodic jobs effortlessly.**  
✅ **Use Supervisor to keep Celery running in production.**  

🚀 **Now you have everything to configure Celery in any project!**  
Would you like help with **deployment** or **monitoring Celery tasks**? 😊

