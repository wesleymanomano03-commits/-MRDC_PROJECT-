import os
from app_fixed import create_app
from models import db

from apscheduler.schedulers.background import BackgroundScheduler
from utils.reminders import check_renewals

app = create_app()

def run_reminders():
    with app.app_context():
        check_renewals()

scheduler = BackgroundScheduler()
scheduler.add_job(func=run_reminders, trigger="interval", hours=24)
scheduler.start()

if __name__ == '__main__':
    os.makedirs('instance', exist_ok=True)
    with app.app_context():
        print("Reminder scheduler started (checks daily).")
    app.run(debug=True)

