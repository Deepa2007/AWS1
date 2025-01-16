import json
import boto3
import base64
from botocore.exceptions import NoCredentialsError

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Extract file details from the event
    file_name = event.get('file_name')
    file_data_base64 = event.get('file_data')  # Base64 encoded file data
    bucket_name = event.get('bucket_name')
    
    if not file_name or not file_data_base64 or not bucket_name:
        return {
            'statusCode': 400,
            'body': json.dumps('file_name, file_data, and bucket_name must be provided')
        }

    # Decode the file data from base64
    try:
        file_data = base64.b64decode(file_data_base64)
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Error decoding file data: {str(e)}')
        }

    # Upload the file to S3
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_data
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f'File {file_name} uploaded successfully to {bucket_name}')
        }
    except NoCredentialsError:
        return {
            'statusCode': 403,
            'body': json.dumps('Access Denied: AWS credentials not found')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error uploading file to S3: {str(e)}')
        }
