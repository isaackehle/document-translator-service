from botocore.exceptions import ClientError

from app.core.clients import s3_client
from app.core.config import settings


def create_buckets() -> None:
    for bucket in (settings.SOURCE_BUCKET, settings.TRANSLATED_BUCKET):
        try:
            s3_client.create_bucket(Bucket=bucket)
        except ClientError as e:
            if e.response.get("Error", {}).get("Code") != "BucketAlreadyOwnedByYou":
                raise


def save_source_file_to_s3(content: bytes, filename: str, content_type: str):
    # Upload to S3
    s3_client.put_object(Bucket=settings.SOURCE_BUCKET, Key=filename, Body=content, ContentType=content_type)
