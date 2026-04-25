from botocore.exceptions import ClientError

from app.core.clients import s3_client
from app.core.config import settings


def create_buckets() -> None:
    for bucket in (settings.SOURCE_BUCKET, settings.TRANSLATED_BUCKET):
        try:
            s3_client.create_bucket(Bucket=bucket)
        except ClientError as e:
            if e.response["Error"]["Code"] != "BucketAlreadyOwnedByYou":
                raise
