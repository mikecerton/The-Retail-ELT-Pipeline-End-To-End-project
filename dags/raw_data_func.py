import os 
import boto3
from dotenv import load_dotenv
import pandas as pd
from io import StringIO

def upload_s3():

    load_dotenv("/opt/airflow/.env")

    bucket_name = os.getenv("bucket_name")
    session = boto3.Session(
        aws_access_key_id = os.getenv("aws_access_key_id"),
        aws_secret_access_key = os.getenv("aws_secret_access_key"),
        region_name = os.getenv("region_name"))

    s3 = session.client('s3')

    with open("/opt/airflow/my_data/Demo_sales_data.csv", "rb") as f:
        s3.upload_fileobj(f, bucket_name, "my_retail_s3.csv")
    print("!_S3_upload_complete_onlineII.csv!")

def download_s3_clean():

    load_dotenv("/opt/airflow/.env")

    bucket_name = os.getenv("bucket_name")
    session = boto3.Session(
        aws_access_key_id = os.getenv("aws_access_key_id"),
        aws_secret_access_key = os.getenv("aws_secret_access_key"),
        region_name = os.getenv("region_name"))

    s3 = session.client('s3')

    # get data from s3
    key = "my_retail_s3.csv"
    dest_path = "/opt/airflow/my_data/my_retail_s3.csv"
    response = s3.get_object(Bucket=bucket_name, Key=key)
    file_content = response['Body'].read().decode('utf-8')

    # clean data
    df = pd.read_csv(StringIO(file_content))
    print(df.isnull().sum())
    df = df.dropna()
    print(df.duplicated().sum())
    df = df.drop_duplicates()
    df.to_csv(dest_path, index=False)


    print("!_S3_download_complete_my_retail_s3.csv!")
    print(f"at {dest_path} !!!")