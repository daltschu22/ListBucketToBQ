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
    parser.add_argument('bucket_name', metavar='gs://bucket-name/', help="Bucket name in google")
    parser.add_argument('--project', dest='project_override', required=False, help="if you want to manually define a project")
    parser.add_argument('--service-account', dest='service_account', required=False, help="service account json")

    return parser.parse_args()

def initiate_storage_client(credentials):
    # print("Initializing google storage client...")
    try:
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
    service_account = args.service_account

    if project_override:
        PROJECT = project_override

    if service_account:
        SERVICE_ACCOUNT = service_account

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    # Initialize the storage client
    storage_client = initiate_storage_client(credentials)

    service_account_name = storage_client.get_service_account_email(PROJECT)

    stuff = "{} - {}".format(bucket_name, service_account_name)

    new_blob = storage_client.bucket.blob('testing123')

    print("uploading object to bucket {}".format(stuff))

    new_blob.upload_from_string(stuff)



if __name__ == "__main__":
    main()
