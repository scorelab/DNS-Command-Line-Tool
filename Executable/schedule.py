from datetime import datetime
import time
import os
from google.cloud import storage
import os
from apscheduler.schedulers.background import BackgroundScheduler

def main_scheduler():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_app_cred.json"
    def tick():
        print('The time is: %s' %datetime.now())

        bucket_object = 'dnstest_bucket_1'
        blob = 'blob_dns'
        storage_client = storage.Client()
 
        bucket = storage_client.bucket(bucket_object)
        blob = bucket.blob(blob)
        blob.download_to_filename('results.json')
    
        print(
            "Blob {} downloaded to file path successfully ".format(
                blob
            )
        )
        print("Upto date")

    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, trigger='interval', minutes=10)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown() 

main_scheduler()