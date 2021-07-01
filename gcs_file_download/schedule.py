# from datetime import datetime, timedelta, time, date
from datetime import datetime
import time
import os
from subprocess import Popen

def background_schedule():
    from apscheduler.schedulers.background import BackgroundScheduler

    def update():
        
        print('The time is: %s' %datetime.now())
        Popen('python3 large_file_download.py')
        print("The dataset is now upto date in your local machine \n")

    scheduler = BackgroundScheduler()

    scheduler.start()

    scheduler.add_job(update, trigger='interval', days=1)
    
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown() 

background_schedule() 