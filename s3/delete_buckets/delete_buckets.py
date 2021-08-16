import boto3
import os
import pandas as pd
import openpyxl
import datetime

# Get date
today = datetime.datetime.now()
removal_date = str(today.strftime("%d%m%Y-%H%M%S"))

# Files
xls_file = "deleted-buckets-" + removal_date + ".xlsx"
bucket_list_file = "./bucket_list.txt"

# List to use in DataFrame
rows = []
    
# Open bucket_list.txt
with open(bucket_list_file) as f:
    bucket_list = f.read().splitlines()

# Set AWS Account
aws_account = input("Digite a conta AWS: ")

# Resource session
def resource_session():
    session = boto3.session.Session(profile_name=aws_account)
    s3 = session.resource('s3')
    return s3

# Verify if bucket exists
def bucket_exists(bucket):
    s3 = resource_session()
    return s3.Bucket(bucket) in s3.buckets.all()

# Count objects of bucket
def total_objects(bucket):
    s3 = resource_session()
    total = 0

    for key in s3.Bucket(bucket).object_versions.all():
        total += 1
    return total

# Remove objects from bucket
def remove_objects(bucket):
    try:
        while (total_objects(bucket)) > 0:
            s3 = resource_session()
            print("Apagando arquivos do bucket: " + bucket)
            b = s3.Bucket(bucket)
            b.object_versions.delete()
    except:
        print("Erro ao tentar listar objetos")

# Delete bucket
def delete_bucket(bucket):
    deleted = False
    session = boto3.session.Session(profile_name=aws_account)
    s3 = session.client('s3')
    print("Deletando bucket: " + bucket)
    try:
        s3.delete_bucket(Bucket=bucket)
        deleted = True
    except:
        print("O bucket " + bucket + " não foi deletado")
    return deleted

# Verify and remove buckets
for bucket in bucket_list:
    bucket_name = bucket
    if bucket_exists(bucket):
        remove_objects(bucket)
        if delete_bucket(bucket) == True:
            rows.append([aws_account, bucket_name, removal_date])
    else:
        print("Bucket " + bucket + " não existe na conta " + aws_account)

df1 = pd.DataFrame(rows, columns=["aws_account", "bucket_name", "removal_date"])
df1.to_excel(xls_file)