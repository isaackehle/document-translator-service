import boto3
from botocore.config import Config
from mypy_boto3_s3 import S3Client

S3_CONFIG = {
    "endpoint_url": "http://localhost:9000",
    "aws_access_key_id": "minioadmin",
    "aws_secret_access_key": "minioadmin",
    "config": Config(signature_version="s3v4", s3={"addressing_style": "path"}),
}

s3_client: S3Client = boto3.client("s3", **S3_CONFIG)


def get_s3_client() -> S3Client:
    return boto3.client("s3", **S3_CONFIG)
