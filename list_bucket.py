#!/usr/bin/env python

import os
import argparse
from google.cloud import storage
import google.cloud.exceptions
from google.oauth2 import service_account
import json

PROJECT = os.environ.get('GCP_PROJECT')
# SERVICE_ACCOUNT = os.environ.get('')

def parse_arguments():
    parser = argparse.ArgumentParser(description="List bucket and dump ls info to bigquery")
    parser.add_argument('bucket_name', metavar='bucket-name', help="Bucket name in google")
    parser.add_argument('--project', dest='project_override', required=False, help="if you want to manually define a project")
    parser.add_argument('--service-account-json', dest='service_account_json', required=False, help="service account json")

    return parser.parse_args()

def initiate_storage_client(credentials=None):
    # print("Initializing google storage client...")
    try:
        if credentials:
            storage_client = storage.Client(project=PROJECT, credentials=credentials)
        else:
            storage_client = storage.Client(project=PROJECT)
        return storage_client
    except Exception as e:
        print("ERROR: Could not connect to storage API!: {}".format(e))

def get_bucket(storage_client, bucket):
    try:
        bucket_object = storage_client.get_bucket(bucket)
        return bucket_object
    except google.cloud.exceptions.NotFound:
        print('ERROR: Requested bucket doesnt exist!')

def billing_upload_byfs_to_bigquery_historical(storage_client, bucket, file_to_upload):
    """Import the provided billing dict to bigquery table for historical purposes."""


    # print("\nUploading filesystem data to bigquery...")
    # # Insert the newline delimeted json file to bucket, cloud function will grab this and put in bq
    # g.storage().insert_object(
    #     'bits-bitstore-json-billing-data-ingest',
    #     'broad_bitstore_app/bits_billing_byfs_bitstore_historical.json',
    #     '\n'.join(row_list)
    # )

def main():
    args = parse_arguments()  # Parse arguments

    bucket_name = args.bucket_name
    project_override = args.project_override
    service_account_json = args.service_account_json

    if project_override:
        PROJECT = project_override

    if service_account_json:
        SERVICE_ACCOUNT = service_account_json
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        # Initialize the storage client
        storage_client = initiate_storage_client(credentials)
    else:
        # Initialize the storage client
        storage_client = initiate_storage_client()


    # working_bucket = get_bucket(storage_client, bucket_name)

    blob_list = storage_client.list_blobs(bucket_name)

    with open('{}.list'.format(bucket_name), 'w') as outfile:
        for blob in blob_list:

            blob_dir = {}
            blob_dir['bucket'] = blob.bucket.name
            blob_dir['time_created'] = blob.time_created.strftime('%Y-%m-%d %H:%M:%S')
            blob_dir['time_updated'] = blob.updated.strftime('%Y-%m-%d %H:%M:%S')
            blob_dir['storage_class'] = blob.storage_class
            blob_dir['content_type'] = blob.content_type
            blob_dir['content_language'] = blob.content_language
            blob_dir['hash_md5'] = blob.md5_hash
            blob_dir['hash_crc'] = blob.crc32c
            blob_dir['etag'] = blob.etag
            blob_dir['generation'] = blob.generation
            blob_dir['metageneration'] = blob.metageneration
            blob_dir['size'] = blob.size
            blob_dir['name'] = blob.name
            blob_dir['url'] = blob.path
            blob_dir['id'] = blob.id

            print(blob_dir)

            blob_json = json.dumps(blob_dir)

            outfile.write('{}\n'.format(blob_json))

            quit()

if __name__ == "__main__":
    main()

