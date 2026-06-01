"""Document API endpoints."""

import uuid
from pathlib import Path

from botocore.exceptions import ClientError
from fastapi import APIRouter, HTTPException, UploadFile, status
from pydantic import BaseModel

from app.core.buckets import save_source_file_to_s3

router = APIRouter()


class Document(BaseModel):
    message: str
    key: str


@router.post(
    "/",
    response_model=Document,
    status_code=status.HTTP_201_CREATED,
    summary="Document upload",
)
def upload_document(file: UploadFile) -> Document:
    """
    Upload a document to S3.

    Args:
        file: The file to upload.

    Returns:
        Document: Information about the uploaded document.

    Raises:
        HTTPException: 500 if there was an error with the upload.
    """
    try:
        # Generate a unique filename to avoid collisions
        original_filename = file.filename or "upload"
        extension = Path(original_filename).suffix
        unique_filename = f"{uuid.uuid4()}{extension}"

        # Read file content (synchronous read for 'def' endpoint)
        content = file.file.read()

        # Upload to S3
        save_source_file_to_s3(
            content, 
            unique_filename, 
            file.content_type or "application/octet-stream"
        )

        return Document(message="Success", key=unique_filename)
    except ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )