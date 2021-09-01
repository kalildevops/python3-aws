#!/usr/bin/env python
import boto3

BUCKET = 'my_bucket'

# Verify if bucket exists
def bucket_exists(bucket):
    s3 = boto3.resource('s3')
    return s3.Bucket(bucket) in s3.buckets.all()

# Count objects of bucket
def total_objects(bucket):
    s3 = boto3.resource('s3')
    total = 0

    for key in s3.Bucket(bucket).object_versions.all():
        total += 1
    return total

if bucket_exists(BUCKET):
    while (total_objects(BUCKET)) > 0:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(BUCKET)
        bucket.object_versions.delete()