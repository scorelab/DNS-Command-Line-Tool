from datetime import datetime
import time
import os
from google.cloud import storage
import logging
from apscheduler.schedulers.background import BackgroundScheduler

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_app_cred.json"

# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG) 

bucket_name = 'dnstest_bucket_1' 
blob_path = 'sync/' # blob path in bucket where data is stored 
local_dir = 'Rsync' 


def main_scheduler():
    def tick():

        print('The time is: %s' %datetime.now())

        bucket_name = 'dnstest_bucket_1' 
        blob_path = 'sync/' # blob path in bucket where data is stored 
        local_path = 'Local Dir' 
            
        if not os.path.exists(local_path):
            os.makedirs(local_path)      

        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blobs=list(bucket.list_blobs(prefix=blob_path))

        startloc = 0
        for blob in blobs:
            startloc = 0
            folderloc = [i for i, letter in enumerate(blob.name.replace(blob_path, '')) if letter == '/']
            if(not blob.name.endswith("/")):
                if(blob.name.replace(blob_path, '').find("/") == -1):
                    downloadpath=local_path + '/' + blob.name.replace(blob_path, '')
                    logging.info(downloadpath)
                    blob.download_to_filename(downloadpath)
                else:
                    for folder in folderloc:
                        
                        if not os.path.exists(local_path + '/' + blob.name.replace(blob_path, '')[startloc:folder]):
                            create_folder=local_path + '/' +blob.name.replace(blob_path, '')[0:startloc]+ '/' +blob.name.replace(blob_path, '')[startloc:folder]
                            startloc = folder + 1
                            os.makedirs(create_folder)
                        
                    downloadpath=local_path + '/' + blob.name.replace(blob_path, '')

                    blob.download_to_filename(downloadpath)
                    
                    logging.info(blob.name.replace(blob_path, '')[0:blob.name.replace(blob_path, '').find("/")])

        # logging.info('Blob {} downloaded to {}.'.format(blob_path, local_path))




    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, trigger='interval', minutes=1)
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