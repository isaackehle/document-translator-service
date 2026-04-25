import boto3
from botocore.config import Config

S3_CONFIG = {
    "endpoint_url": "http://localhost:9000",
    "aws_access_key_id": "minioadmin",
    "aws_secret_access_key": "minioadmin",
    "config": Config(signature_version="s3v4", s3={"addressing_style": "path"}),
}

# Create a single, reusable S3 client instance
s3_client = boto3.client("s3", **S3_CONFIG)


# You can also create a function to get the client if needed
def get_s3_client():
    return boto3.client("s3", **S3_CONFIG)
