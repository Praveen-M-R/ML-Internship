from celery import Celery
from celery.schedules import crontab
from date_filling import update_filing_dates

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@app.task
def scheduled_task():
    update_filing_dates(['8-K', '10-K', '10-Q'])
    return "Task executed successfully"

# Define a periodic task schedule
app.conf.beat_schedule = {
    'run-every-1-minute': {
        'task': 'tasks.scheduled_task',
        'schedule': 100.0,  # Run every 60 seconds
    },
}
app.conf.timezone = 'UTC'
