import argparse 
from google.cloud import storage
from google.oauth2 import service_account
import os

app_cred_dict = {
  "type": "service_account",
  "project_id": "daring-chess-315909",
  "private_key_id": "30b7afd724d1c14787de0737b34169013085b82c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDE+z+nCeD+LhEQ\nGuYvZtfq44Gt5eu86ltb5yHxw23Um4+frKvkLixP+0tzmTGJeFl45SCs9wOiwL6Q\nAqSi9AB2EXPUph6tf/29LpTZ6zNVq1QhHJhATbIDbQW6BZE9kM7Edju8F3pFRaqq\n0T5eDPaOvAEDcJWudm9BLEnpI5z1ws2fag4VT0GOp3TYTZc9Gwx24EbeQMgiTX6s\n/U1FyfmX1s4KxyCRabsMjK2CMleHq6+jI1N2pyRWXnTx2Wlfu4U65d8cVkxVa5zN\nhlS2jOYFEZBIzpNeSD+aOlnshVKGSxE+Pl8s/h8Jfbx+RunjFcdCBADyKwIPcjZw\nVsTC8vmrAgMBAAECggEADC1qIHX0YlJPvLqk+040z/ETncAGhE3KqxJNX2hQ/GFH\njjv6/ma6V5F19yYD0XdOtLIZhIfawi9/OGDpc6d49dObYQyJ/fjZI15jVlt7d3LZ\nhxiA8wy6kgql3XuloHQ4zB1xEO40oV6ur9OystbDUUyfFWra3ge1VgaaZR7N/8VY\nz/K3GW4OxmN+Ydu58TQC7GBfe06tbqqAccZ0AYW701QZVORnKQHymwDA98KjSYFR\nMdZ++/dpjVcqs6LyJXDiuljPBnp/y7+g7PMmO8aDjm3jy59VElcV+CPx+KerYcGN\n9MfQlXvZ14fFw1Bch1C/AI326pgwcIZAP9yc84BNiQKBgQD4WhJAj9BmZE3FgEmm\nu5xCBVAffL74Ns+8xoEtmv9hr1L1Yk16Zf18avvQi7Jubr4ncNCHnWHg5RB73EQj\nE3egy7BGgiDNpwuH0bG7H4wgokat63lVt0MHnwB2YNHfHmQ0dsYRFVT+mzzUe9PU\nkBYWjDhxlk/Wf81M3YqoBExEAwKBgQDLDDBnLoqARmt0bojVTvsJ/BSqMnRmyZiK\noFKfv2gYZN7rZLl20Sd1gv4VMq2XY2LzknsvBbJ654M8jF1GBU4F6JaYbR+1s29c\nsgYgZye8cthkVqCL/iUDdYdpXkroDYR/z4pqokOpBAekDAvIip374g8z9LKSGWkG\nodASwQlHOQKBgQCwdC6ruIK1fWbUgMXTtVDch7HZ7WQyL5+B3PhDUvFIkq06s9Gg\nuX5VPB4Wmmr4k65/j2RaNrQoehgwKNwwn9BLau2f6y0rcRh8M7032r5RIXtebwQS\nptb1Pz+w3DHBeXJw5ELuOF3fWKTrw99KE+Xdt1sTOV0YZk2T44R0xDj7yQKBgC6E\nPlqFGQnGGDv2Tra/f1eMPpe3M1+Q87def09FpG1iPoei7bJAvE95kQf+MjKqfDLc\n7geZwIfTngczCPNPp85GuKl25nrT/sE3r5ugxkOv888Y4XLw6D3goQMMrRB4eFBn\nlYhUYDfKSo3UjKaGyya3ZVA70OUTmTIBxA9n1d5RAoGBAKm1hCL0zgzm2mrlKjOa\nstwAplqrcGppPL9eZJiDGmDXrpudCpdfky45HLxeMgnC9RMNZdhF67T10bVX/W6W\nGppIAd30+QbJgKfum1jRq9Lip5bsXk5jphF5cyVDPUq5jX9fwOyfa/sHplVEewaZ\nwJETFg/JJ/kYmY29vhDtulBh\n-----END PRIVATE KEY-----\n",
  "client_email": "dnstest@daring-chess-315909.iam.gserviceaccount.com",
  "client_id": "110844357860663711229",
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