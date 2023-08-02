import boto3, botocore
import os
from werkzeug.utils import secure_filename

AWS_BUCKET_NAME=os.getenv('AWS_BUCKET_NAME')
AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY=os.getenv('AWS_SECRET_KEY')
AWS_LOCATION=os.getenv('AWS_LOCATION')

def upload_file_to_s3(file, acl="public-read"):
    
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    filename = secure_filename(file.filename)
    try:
        s3.upload_fileobj(
            file,
            AWS_BUCKET_NAME,
            filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Error: ", e)
        return e
    return file.filename


def read_files_from_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    objs = s3.list_objects(Bucket = AWS_BUCKET_NAME)['Contents']
    [obj['Key'] for obj in objs if obj['Size']]
    print(objs)