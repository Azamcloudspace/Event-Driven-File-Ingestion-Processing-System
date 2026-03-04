import json
import boto3
import os

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])

        bucket = body["detail"]["bucket"]["name"]
        key = body["detail"]["object"]["key"]

        file_obj = s3.get_object(Bucket=bucket, Key=key)
        size = file_obj["ContentLength"]

        table.put_item(
            Item={
                "FileName": key,
                "Bucket": bucket,
                "Size": size
            }
        )

    return {"statusCode": 200}