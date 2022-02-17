import argparse 
from google.cloud import storage
from google.oauth2 import service_account
import os
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

def blob_size(bucket_name, source_blob_name):

    storage_client = storage.Client(project=app_cred_dict['project_id'],credentials=credentials)
 
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(source_blob_name)
    blobSize = blob.size
    print('Downloadable dataset size: '+ str(blobSize))


def list_data(bucket_name,blob_path):
    storage_client = storage.Client(project=app_cred_dict['project_id'],credentials=credentials)
    bucket = storage_client.get_bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=blob_path))

    for blob in blobs:
        print(blob.name)


def last_update(bucket_name,blob_path):

    storage_client = storage.Client(project=app_cred_dict['project_id'],credentials=credentials)
 
    bucket = storage_client.bucket(bucket_name)
    # blob = bucket.get_blob(source_blob_name)
    blobs = list(bucket.list_blobs(prefix=blob_path))
    for blob in blobs:
        print("{} updated on: {}".format(blob.name,blob.updated))

def download_blob(bucket_name, source_blob_name, dest_file):
    storage_client = storage.Client(project=app_cred_dict['project_id'],credentials=credentials)
 
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(dest_file)
 
    print(
        "Blob {} downloaded to file path {} successfully ".format(
            source_blob_name, dest_file
        )
    )


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


bucket_object = 'dnstest_bucket_1'
blob = 'blob_dns'
blob_path = 'sync/'


parser = argparse.ArgumentParser(description='Check, download and update the local DNS IP dataset location.')

# Add argument
parser.add_argument('--size', action='store_const',const='True', help="The size of the downloadable blob")

parser.add_argument('--list' ,  action='store_const',const='True',help="List the available data for downloading")

parser.add_argument('--last_update' , action='store_const',const='True', help="See when the dataset was last updated")

parser.add_argument('--download' , help="Download a single file")

parser.add_argument('--download_bucket' , help="One-time download of the complete DNSIP dataset")

args = vars(parser.parse_args())

# print(args)

if args.get('size'):
    blob_size(bucket_object,blob)


if args.get('list'):
    list_data(bucket_object,blob_path)


if args.get('last_update'):
    last_update(bucket_object,blob_path)

if args.get('download'):
    dest_file = args['download']
    download_blob(bucket_object,blob,dest_file)

if args.get('download_bucket'):
    dest_folder = args['download_bucket']
    download_bucket(bucket_object,dest_folder)