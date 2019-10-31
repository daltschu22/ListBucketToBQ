#!/usr/bin/env python

import os
import argparse
from google.cloud import storage, logging
import google.cloud.exceptions

PROJECT = os.environ.get('GCP_PROJECT')


def parse_arguments():
    parser = argparse.ArgumentParser(description="List bucket and dump ls info to bigquery")
    parser.add_argument('bucket_name', metavar='gs://bucket-name/', help="Bucket name in google")

    return parser.parse_args()

def initiate_storage_client():
    # print("Initializing google storage client...")
    try:
        storage_client = storage.Client(project=PROJECT)
        return storage_client
    except Exception as e:
        logging.warn("ERROR: Could not connect to storage API!: {}".format(e))

def get_bucket(storage_client, bucket):
    try:
        bucket_object = storage_client.get_bucket(bucket)
        return bucket_object
    except google.cloud.exceptions.NotFound:
        logging.warn('ERROR: Requested bucket doesnt exist!')

def main():
    # Initialize the storage client
    storage_client = initiate_storage_client()

    args = parse_arguments()  # Parse arguments

    bucket_name = args.bucket_name

    service_account_name = storage_client.get_service_account_email()

    stuff = "{} - {}".format(bucket_name, service_account_name)

    new_blob = storage_client.bucket.blob('testing123')

    print("uploading object to bucket {}".format(stuff))

    new_blob.upload_from_string(stuff)



if __name__ == "__main__":
    main()
