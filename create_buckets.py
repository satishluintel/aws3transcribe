# CODE TO CREATE BUCKET

import logging
import boto3
from botocore.exceptions import ClientError
from keys import access_key, secret_access_key


region = 'ap-southeast-1'
bucket_name = ''


def create_bucket(bucket_name, region=region):
    try:
        if region is None:
            s3_client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)
            bucket_name = input("Enter a bucket name of your choice. Please use only lowercase letters and numbers.   ")
            s3_client.create_bucket(Bucket=bucket_name)
            print("SUCCESS !!! Go check your S3 page.\n")
        
        else:
            s3_client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key, region_name=region)
            location = {'LocationConstraint': region}
            bucket_name = input("Enter a bucket name of your choice. Please use only lowercase letters and numbers.   ")
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
            print("SUCCESS !!! Go check your S3 page.\n")
    
    except ClientError as e:
        logging.error(e)
        print("Something happened, please try using a different name for bucket.\n")
        return False
    return True

s3_client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)
response= s3_client.list_buckets()
print("Found "+ str(len(response["Buckets"])) + " bucket(s) \n" )

# FETCH ALL AVAILABLE BUCKETS UNDER YOUR S3 INSTANCE
for x in range(len(response["Buckets"])):
	print(x," ",response["Buckets"][x]["Name"] )  #print bucket names 


create_bucket(bucket_name)


