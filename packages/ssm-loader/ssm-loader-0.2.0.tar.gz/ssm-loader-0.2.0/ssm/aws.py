import boto3
import os

ssm_client = boto3.client("ssm", region_name=os.environ.get('AWS_REGION', 'us-east-1'))
