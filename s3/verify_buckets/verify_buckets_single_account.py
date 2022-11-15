import boto3
import os
import pandas as pd
import openpyxl
import datetime

# Get date
today = datetime.datetime.now()
date_time = today.strftime("%d%m%Y-%H%M%S")

# Files
xls_file = "all_buckets-" + str(date_time) + ".xlsx"

# List to use in DataFrame
rows = []

# Define aws_account
aws_account = "default"
    
# Configure session:
# session = boto3.session.Session(profile_name=aws_account)
default_session = get_session(disable_env_vars=True)
response = default_session.client('sts').get_caller_identity()

# Get list of buckets and creation date
# this = session.resource('s3')
this = response.resource('s3')

bucket_list = this.buckets.all()
for bucket in bucket_list:
    bucket_name = str(bucket.name)
    creation_date = str(bucket.creation_date)
    print(str(bucket_name) + " " + str(creation_date))

    # s3 = session.client('s3')
    s3 = response.client('s3')

    # Verify if bucket is empty
    try:
        bucket_objects = s3.list_objects_v2(Bucket=bucket_name)
        if bucket_objects['KeyCount'] > 0:
            bucket_objects = "Has content"
            print("Bucket Objects: " + str(bucket_objects))
        else:
            bucket_objects = "Empty"
            print("Bucket Objects: " + str(bucket_objects))
    except:
        bucket_objects = "Error trying to list objects"
    
    # Verify if bucket has policy
    try:
        bucket_policy = s3.get_bucket_policy(Bucket=bucket_name)
        if bucket_policy['Policy'] != "":
            bucket_policy = "Has policy"
            print("Bucket Policy: " + str(bucket_policy))
            
    except:
        bucket_policy = "No policy found"
        print("NoSuchBucketPolicy")
        print("Bucket Policy: " + str(bucket_policy))

    # Verify if bucket has public access BLOCK configuration
    try:
        bucket_type = s3.get_public_access_block(Bucket=bucket_name)
        if bucket_type['PublicAccessBlockConfiguration']['BlockPublicAcls'] == True:
            bucket_block_pub_acls = "Blocks public ACLs"
            block_pub_acls = True
        else:
            bucket_block_pub_acls = "Does not blocks public ACLs"
            block_pub_acls = False
        print("Bucket Block Public ACLs: " + str(bucket_block_pub_acls))

        if bucket_type['PublicAccessBlockConfiguration']['BlockPublicPolicy'] == True:
            bucket_block_pub_policy = "Blocks public Policy"
            block_pub_policy = True
        else:
            bucket_block_pub_policy = "Does not blocks public Policy"
            block_pub_policy = False
        print("Bucket Block Public Policy: " + str(bucket_block_pub_policy))
    except:
        bucket_block_pub_acls = "Does not blocks public ACLs"
        block_pub_acls = False
        bucket_block_pub_policy = "Does not blocks public Policy"
        block_pub_policy = False
        print("NoSuchPublicAccessBlockConfiguration")
        print("Bucket Block Public ACLs: " + str(bucket_block_pub_acls))
        print("Bucket Block Public Policy: " + str(bucket_block_pub_policy))
    
    # Verify bucket policy status
    try:
        bucket_type = s3.get_public_access_block(Bucket=bucket_name)
        bucket_policy_status = s3.get_bucket_policy_status(Bucket=bucket_name)
        if (block_pub_acls and block_pub_policy) == True:
            bucket_policy_status = "private"
            print("Bucket Policy Status: " + str(bucket_policy_status))
        else:
            if bucket_policy_status['PolicyStatus']['IsPublic'] == True:
                bucket_policy_status = "public"
            else:
                bucket_policy_status = "not public"
            print("Bucket Policy Status: " + str(bucket_policy_status))
    except:
        print("NoSuchBucketPolicyStatus")
        if (block_pub_acls and block_pub_policy) == True:
            bucket_policy_status = "private"
            print("Bucket Policy Status: " + str(bucket_policy_status))
        else:
            if (block_pub_acls or block_pub_policy) == False:
                bucket_policy_status = "public"
            else:
                bucket_policy_status = "not public"
            print("Bucket Policy Status: " + str(bucket_policy_status))

    # Verify website configuration
    try:
        bucket_website = s3.get_bucket_website(Bucket=bucket_name)
        if bucket_website != "":
            print(bucket_website)
            bucket_website = "Website hosting enabled"
    except:
        print("NoSuchWebsiteConfiguration")
        bucket_website = "Website hosting disabled"
        print(bucket_website)

    rows.append([
        aws_account,
        bucket_name,
        creation_date,
        bucket_objects,
        bucket_policy_status,
        bucket_policy,
        bucket_block_pub_acls,
        bucket_block_pub_policy,
        bucket_website
    ])

df1 = pd.DataFrame(rows,
columns=[
    "aws_account",
    "bucket_name",
    "creation_date",
    "bucket_objects",
    "bucket_policy_status",
    "bucket_policy",
    "bucket_block_pub_acls",
    "bucket_block_pub_policy",
    "bucket_website"
])

df1.to_excel(xls_file)