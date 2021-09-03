import boto3
import pandas as pd
import datetime

# Get date
today = datetime.datetime.now()
modification_date = str(today.strftime("%d%m%Y"))

# Files
xls_file = "./results/iam-users-" + modification_date + ".xlsx"

# List to use in DataFrame
rows = []
    
# Set AWS Account
aws_account = input("Enter AWS account: ")

# Resource session
def resource_session():
    session = boto3.session.Session(profile_name=aws_account)
    iam = session.resource('iam')
    return iam

# Client session
def client_session():
    session = boto3.session.Session(profile_name=aws_account)
    iam = session.client('iam')
    return iam

def list_users():
    iam = client_session()
    paginator = iam.get_paginator('list_users')
    for response in paginator.paginate():
        for user in response["Users"]:
            rows.append([aws_account, user['UserName']])

list_users()

# Create .xlsx
df1 = pd.DataFrame(rows, columns=["AWS_Account", "Username"])
df1.to_excel(xls_file)
