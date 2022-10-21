import boto3

from fastapi import HTTPException, status

AWS_KEY_ID = ""  # enter your key id
AWS_ACCESS_KEY = ""  # enter your access key
BUCKET_NAME = ""  # enter your bucket name


def get_link(photo):

    s3 = boto3.resource("s3", aws_access_key_id=AWS_KEY_ID,
                        aws_secret_access_key=AWS_ACCESS_KEY)
    bucket = s3.Bucket(BUCKET_NAME)
    bucket.upload_fileobj(photo.file, photo.filename, ExtraArgs={
        "ACL": "public-read"
    })

    try:
        s3.Object(BUCKET_NAME, photo.filename).load()  # calls s3.client.head_object()
    except:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    return f"https://{BUCKET_NAME}.s3.amazonaws.com/{photo.filename}"
