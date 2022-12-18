from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import getinfo

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(getinfo, 'interval',hours=4)
    scheduler.start()