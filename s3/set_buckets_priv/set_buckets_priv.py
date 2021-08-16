import boto3
import pandas as pd
import datetime

# Get date
today = datetime.datetime.now()
modification_date = str(today.strftime("%d%m%Y-%H%M%S"))

# Files
xls_file = "./results/changed-buckets-" + modification_date + ".xlsx"
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

# Client session
def client_session():
    session = boto3.session.Session(profile_name=aws_account)
    s3 = session.client('s3')
    return s3

# Verify if bucket exists
def bucket_exists(bucket):
    s3 = resource_session()
    return s3.Bucket(bucket) in s3.buckets.all()

# Verify if bucket has public access BLOCK configuration
def has_block_configuration(bucket):
    s3 = client_session()
    private = False
    try:
        bucket_type = s3.get_public_access_block(Bucket=bucket)
        if bucket_type['PublicAccessBlockConfiguration']['BlockPublicAcls'] == True:
            block_pub_acls = True
        else:
            block_pub_acls = False

        if bucket_type['PublicAccessBlockConfiguration']['BlockPublicPolicy'] == True:
            block_pub_policy = True
        else:
            block_pub_policy = False

        if (block_pub_acls == True) and (block_pub_policy == True):
            private = True
    except:
        block_pub_acls = False
        block_pub_policy = False
        print("NoSuchPublicAccessBlockConfiguration")
    return private
    

# Set bucket private
def set_bucket_private(bucket):
    s3 = client_session()
    changed = False
    try:
        s3.put_public_access_block(
            Bucket=bucket,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        changed = True
        print("Bucket " + bucket + " alterado para privado")
    except:
        print("Não foi possível converter o bucket " + bucket + " para privado")
    return changed


# Verify and convert public buckets to private
for bucket in bucket_list:
    bucket_name = bucket
    if (bucket_exists(bucket)) and (has_block_configuration(bucket) == False):
        if set_bucket_private(bucket) == True:
            rows.append([aws_account, bucket_name, modification_date])
    else:
        print("Bucket " + bucket + " não existe na conta " + aws_account + " ou já está privado")

df1 = pd.DataFrame(rows, columns=["aws_account", "bucket_name", "modification_date"])
df1.to_excel(xls_file)