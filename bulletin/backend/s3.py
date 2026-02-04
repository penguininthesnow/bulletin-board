import boto3
import uuid
import os

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AES_REGION"),
)

BUCKET = os.getenv("s3_BUCKET")
CLOUDFRONT_URL = os.getenv("CLOUDFRONT_URL")


def upload_image(file):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    s3.upload_fileobj(
        file.file, BUCKET, filename, ExtraArgs={"ContentType": file.content_type}
    )

    return f"{CLOUDFRONT_URL}/{filename}"
