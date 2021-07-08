import argparse 
from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_app_cred.json"

def blob_size(bucket_name, source_blob_name):

    storage_client = storage.Client()
 
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(source_blob_name)
    blobSize = blob.size
    print('Downloadable dataset size: '+ str(blobSize))


def list_data(bucket_name):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        print(blob.name)


def last_update(bucket_name):

    storage_client = storage.Client()
 
    bucket = storage_client.bucket(bucket_name)
    # blob = bucket.get_blob(source_blob_name)
    blobs = storage_client.list_blobs(bucket)
    for blob in blobs:
        print("{} updated on: {}".format(blob.name,blob.updated))

def download_blob(bucket_name, source_blob_name, dest_file):
    storage_client = storage.Client()
 
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(dest_file)
 
    print(
        "Blob {} downloaded to file path {} successfully ".format(
            source_blob_name, dest_file
        )
    )


def download_bucket(bucket_name,dest_folder):
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        with open(os.path.join(dest_folder, str(blob.name)), 'w') as fp:
            pass
        blob = bucket.blob(blob.name)
        blob.download_to_filename(dest_folder+'/'+blob.name)
 
        print(
            "Blob {} downloaded to file path {} successfully ".format(
                blob.name, dest_folder
            )
        )



bucket_object = 'dnstest_bucket_1'
blob = 'blob_dns'


parser = argparse.ArgumentParser(description='Check, download and update the local DNS IP dataset location.')

# Add argument
parser.add_argument('--size', action='store_const',const='True', help="The size of the downloadable blob")

parser.add_argument('--list' ,  action='store_const',const='True',help="List the available data for downloading")

parser.add_argument('--last_update' , action='store_const',const='True', help="See when the dataset was last updated")

parser.add_argument('--download' , help="First time download of the DNS IP blob")

parser.add_argument('--download_bucket',help="First time download of the DNS IP dataset")

args = vars(parser.parse_args())

# print(args)

if args.get('size'):
    blob_size(bucket_object,blob)


if args.get('list'):
    list_data(bucket_object)


if args.get('last_update'):
    last_update(bucket_object)

if args.get('download'):
    dest_file = args['download']
    download_blob(bucket_object,blob,dest_file)

if args.get('download_bucket'):
    dest_folder = args['download_bucket']
    download_bucket(bucket_object,dest_folder)