import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

class AWS_S3:
    def __init__(self):
        load_dotenv()
        self.region = os.getenv("AWS_REGION", "ap-southeast-1")
        self.bucket_name = os.getenv("S3_BUCKET_NAME")
        
        # Initialize the S3 client
        self.s3_client = boto3.client('s3', region_name=self.region)

    def generate_presigned_get_url(self, object_key: str, expiration=3600):
        """Generate a presigned URL to view/download an object from S3."""
        if not object_key:
            return None
            
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_key},
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            print(f"Error generating presigned GET URL: {e}")
            return None

    def generate_presigned_put_url(self, object_key: str, content_type: str, expiration=3600):
        """Generate a presigned URL to upload an object to S3."""
        try:
            response = self.s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_key,
                    'ContentType': content_type
                },
                ExpiresIn=expiration
            )
            return {"uploadUrl": response, "key": object_key}
        except ClientError as e:
            print(f"Error generating presigned PUT URL: {e}")
            return None
