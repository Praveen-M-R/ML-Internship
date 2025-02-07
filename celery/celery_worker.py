from celery_config import celery  # Import Celery instance
import tasks  # Import the tasks module (no direct Celery import needed)


if __name__ == "__main__":
    celery.start()
