#!/usr/bin/env python

import os
import argparse
from google.cloud import storage
import google.cloud.exceptions
from google.oauth2 import service_account

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

    service_account_name = storage_client.get_service_account_email(PROJECT)

    stuff = "{} - {}".format(bucket_name, service_account_name)

    working_bucket = get_bucket(storage_client, bucket_name)

    new_blob = working_bucket.blob('testing123')

    print("uploading object to bucket {}".format(stuff))

    new_blob.upload_from_string(stuff)



if __name__ == "__main__":
    main()
