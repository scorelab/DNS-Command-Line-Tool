from datetime import datetime
import time
import os
from google.cloud import storage
from google.oauth2 import service_account
import logging
from apscheduler.schedulers.background import BackgroundScheduler

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

# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG) 

bucket_name = 'dnstest_bucket_1'
blob_path = 'sync/'  # blob path in bucket where data is stored
local_dir = 'Rsync'


def main_scheduler():
    def tick():

        print('The time is: %s' % datetime.now())

        bucket_name = 'dnstest_bucket_1'
        blob_path = 'sync/'  # blob path in bucket where data is stored
        local_path = 'Local Dir'

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
                    logging.info(downloadpath)
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

                    logging.info(blob.name.replace(blob_path, '')[0:blob.name.replace(blob_path, '').find("/")])

        logging.info('Blob {} downloaded to {}.'.format(blob_path, local_path))

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