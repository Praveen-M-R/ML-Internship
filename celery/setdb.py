# Initialize Celery
app = Celery("sec_scraper", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")
app.conf.timezone = "UTC"

BEAT_DB_PATH = "celerybeat-schedule.db"
if not os.path.exists(BEAT_DB_PATH):
    logging.warning(f"{BEAT_DB_PATH} not found. It will be created on first run.")

# Configure Celery Beat to store schedules in SQLite
app.conf.update(
    beat_schedule_filename=BEAT_DB_PATH
)
