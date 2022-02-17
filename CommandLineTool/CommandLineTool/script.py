import argparse 
from google.cloud import storage
from google.oauth2 import service_account
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

from dotenv import load_dotenv

load_dotenv()

app_cred_dict = {
  "type": "service_account",
  "project_id": os.getenv('PROJECT_ID'),
  "private_key_id": os.getenv('PRIVATE_KEY_ID'),
  "private_key": os.getenv('PRIVATE_KEY'),
  "client_email": os.getenv('CLIENT_EMAIL'),
  "client_id": os.getenv('CLIENT_ID'),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dnstest%40daring-chess-315909.iam.gserviceaccount.com"
}

credentials = service_account.Credentials.from_service_account_info(app_cred_dict)

def blob_size(bucket_name, blob_path):

    storage_client = storage.Client(project=app_cred_dict['project_id'],credentials=credentials)
 
    bucket = storage_client.bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=blob_path))
    total_size = 0
    for blob in blobs:
        blobSize = blob.size
        total_size = total_size + blobSize
    print('Downloadable content size: '+ str(total_size))


def list_data(bucket_name,blob_path):
    storage_client = storage.Client(project=app_cred_dict['project_id'],credentials=credentials)
    bucket = storage_client.get_bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=blob_path))

    for blob in blobs:
        print(blob.name)


def last_update(bucket_name,blob_path):

    storage_client = storage.Client(project=app_cred_dict['project_id'],credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=blob_path))
    for blob in blobs:
        print("{} updated on: {}".format(blob.name,blob.updated))


def download_bucket(bucket_name,local_path):
    if not os.path.exists(local_path):
        os.mkdir(local_path)
    storage_client = storage.Client(project=app_cred_dict['project_id'],credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blobs = storage_client.list_blobs(bucket_name)

    startloc = 0
    for blob in blobs:
        startloc = 0
        folderloc = [i for i, letter in enumerate(blob.name.replace(blob_path, '')) if letter == '/']
        if (not blob.name.endswith("/")):
            if (blob.name.replace(blob_path, '').find("/") == -1):
                downloadpath = local_path + '/' + blob.name.replace(blob_path, '')
                blob.download_to_filename(downloadpath)
            else:
                for folder in folderloc:
                    if not os.path.exists(local_path + '/' + blob.name.replace(blob_path, '')[startloc:folder]):
                        create_folder = local_path + '/' + blob.name.replace(blob_path, '')[
                                                           0:startloc] + '/' + blob.name.replace(blob_path, '')[
                                                                               startloc:folder]
                        startloc = folder + 1
                        os.makedirs(create_folder)

                downloadpath = local_path + '/' + blob.name.replace(blob_path, '')

                blob.download_to_filename(downloadpath)


def main_scheduler(bucket_name,local_path):
    def tick():

        print('The time is: %s' % datetime.now())

        blob_path = 'sync/'  # blob path in bucket where data is stored

        if not os.path.exists(local_path):
            os.makedirs(local_path)

        storage_client = storage.Client(project=app_cred_dict['project_id'], credentials=credentials)
        bucket = storage_client.get_bucket(bucket_name)
        blobs = list(bucket.list_blobs(prefix=blob_path))

        startloc = 0
        for blob in blobs:
            startloc = 0
            folderloc = [i for i, letter in enumerate(blob.name.replace(blob_path, '')) if letter == '/']
            if (not blob.name.endswith("/")):
                if (blob.name.replace(blob_path, '').find("/") == -1):
                    downloadpath = local_path + '/' + blob.name.replace(blob_path, '')
                    # logging.info(downloadpath)
                    blob.download_to_filename(downloadpath)
                else:
                    for folder in folderloc:
                        if not os.path.exists(local_path + '/' + blob.name.replace(blob_path, '')[startloc:folder]):
                            create_folder = local_path + '/' + blob.name.replace(blob_path, '')[
                                                               0:startloc] + '/' + blob.name.replace(blob_path, '')[
                                                                                   startloc:folder]
                            startloc = folder + 1
                            os.makedirs(create_folder)

                    downloadpath = local_path + '/' + blob.name.replace(blob_path, '')

                    blob.download_to_filename(downloadpath)

                    # logging.info(blob.name.replace(blob_path, '')[0:blob.name.replace(blob_path, '').find("/")])

        # logging.info('Blob {} downloaded to {}.'.format(blob_path, local_path))

        for paths, subdirs, files in os.walk(os.path.normpath(local_path), topdown=True):
            for file in files:
                full_path = os.path.join(paths, file)
                normalised = os.path.normpath(full_path)
                file_path = normalised.replace('\\', '/')

                file_path = file_path.replace(local_path, blob_path.replace('/', ''))

                stats = storage.Blob(bucket=bucket, name=file_path).exists(storage_client)

                if stats == False:
                    os.remove(full_path)
                    print('Deleted ' + file_path)

    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, trigger='interval', days=1)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()

bucket_object = 'dnstest_bucket_1'
blob_path = 'sync/'


def main():

    parser = argparse.ArgumentParser(description='Check, download and update the local DNS IP dataset location.')

    # Add argument
    parser.add_argument('--size', action='store_const',const='True', help="The size of the downloadable blob")

    parser.add_argument('--list' ,  action='store_const',const='True',help="List the available data for downloading")

    parser.add_argument('--download', help="Download a single file", metavar='file_to_download')

    parser.add_argument('--download_bucket', help="One-time download of the complete DNSIP dataset",
                        metavar='Local_location_of_files')

    parser.add_argument('--schedule', help='Update the DNSIP dataset every 24 hours' , metavar='Local_location_of_files')

    # print(args)

    args = vars(parser.parse_args())

    if args.get('size'):
        blob_size(bucket_object,blob_path)


    if args.get('list'):
        list_data(bucket_object,blob_path)


    if args.get('last_update'):
        last_update(bucket_object,blob_path)


    if args.get('download_bucket'):
        dest_folder = args['download_bucket']
        download_bucket(bucket_object,dest_folder)

    if args.get('schedule'):
        dest_folder = args['schedule']
        main_scheduler(bucket_object,dest_folder)
