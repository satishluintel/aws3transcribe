# CODE TO DELETE BUCKETs

import logging
import boto3
from botocore.exceptions import ClientError
from keys import access_key, secret_access_key

region = 'ap-southeast-1'  # choose your region here 
bucket_name = ''   #empty bucket name



def delete_bucket(bucket_name, region=None):
    try:
        if region is None:
            s3_client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)
            s3_resource = boto3.resource('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)
            bucket_name = input("Enter a bucket name to delete. ")

            #delete all objects in the bucket
            res = []
            bucket=s3_resource.Bucket(bucket_name)
            for obj_version in bucket.object_versions.all():
                res.append({'Key': obj_version.object_key,'VersionId': obj_version.id})
            print(res)
            bucket.delete_objects(Delete={'Objects': res})

            s3_client.delete_bucket(Bucket=bucket_name)
            print("SUCCESS !!! Go check your S3 page.\n")
        
        else:
            s3_client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key, region_name=region)
            s3_resource = boto3.resource('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key, region_name=region)
            location = {'LocationConstraint': region}
            bucket_name = input("Enter a bucket name to delete. ")

            res = []
            bucket=s3_resource.Bucket(bucket_name)
            for obj_version in bucket.object_versions.all():
                res.append({'Key': obj_version.object_key,'VersionId': obj_version.id})
            print(res)
            bucket.delete_objects(Delete={'Objects': res})


            s3_client.delete_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
            print("SUCCESS !!! Go check your S3 page.\n")
    
    except ClientError as e:
        logging.error(e)
        print("Something happened. Please check your code again or contact the developer.\n")
        return False
    return True


s3_client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)
response= s3_client.list_buckets()
print("Found "+ str(len(response["Buckets"])) + " bucket(s) \n" )

# FETCH ALL AVAILABLE BUCKETS UNDER YOUR S3 INSTANCE
for x in range(len(response["Buckets"])):
	print(x," ",response["Buckets"][x]["Name"] )  #print bucket name

delete_bucket(bucket_name)