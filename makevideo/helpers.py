
import boto3
from botocore.client import Config
from django.conf import settings
from io import BytesIO

def upload_file_to_minio(file_bytes, filename):
    s3_client = boto3.client(
        's3',
        endpoint_url=settings.MINIO_STORAGE['ENDPOINT'],
        aws_access_key_id=settings.MINIO_STORAGE['ACCESS_KEY'],
        aws_secret_access_key=settings.MINIO_STORAGE['SECRET_KEY'],
        config=Config(signature_version='s3v4'),
        region_name='ap-south-1',  # MinIO uses 'us-east-1' by default, can be anything
        verify=True,  # For self-signed certs, set True if using real SSL
    )
    if isinstance(file_bytes, BytesIO):
        file_obj = file_bytes
    else:
        file_obj = BytesIO(file_bytes)
    # Upload file_obj (a file-like object) to bucket with filename/key
    s3_client.upload_fileobj(file_obj, settings.MINIO_STORAGE['BUCKET_NAME'], filename)

    # Return the public URL of the uploaded file if bucket is public
    url = f"{settings.MINIO_STORAGE['ENDPOINT']}{settings.MINIO_STORAGE['BUCKET_NAME']}/{filename}"
    return url

def delete_file_from_minio(filename:str)->bool:
    try:
        s3_client = boto3.client(
            's3',
            endpoint_url=settings.MINIO_STORAGE['ENDPOINT'],
            aws_access_key_id=settings.MINIO_STORAGE['ACCESS_KEY'],
            aws_secret_access_key=settings.MINIO_STORAGE['SECRET_KEY'],
            config=Config(signature_version='s3v4'),
            region_name='ap-south-1',  # MinIO uses 'us-east-1' by default, can be anything
            verify=True,  # For self-signed certs, set True if using real SSL
        )
        s3_client.delete_object(Bucket=settings.MINIO_STORAGE['BUCKET_NAME'], Key=filename)
        return True
    except Exception as e:
        print("failed to delete file")
        print(e)
        return False
