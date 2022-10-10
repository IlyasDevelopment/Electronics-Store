import boto3

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
    return f"https://{BUCKET_NAME}.s3.amazonaws.com/{photo.filename}"
