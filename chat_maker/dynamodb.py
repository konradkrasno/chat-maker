import os
from typing import Dict

import boto3
from botocore.exceptions import ClientError

ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")


class DynamoDBClient:
    def __init__(self, aws_region: str):
        self.aws_region = aws_region

        if ENVIRONMENT == "dev":
            self.dynamodb_host = "http://localhost:4566"
        else:
            self.dynamodb_host = f"https://dynamodb.{aws_region}.amazonaws.com"

        self.dynamodb = boto3.resource("dynamodb", endpoint_url=self.dynamodb_host)

    def get_item(self, item_id: Dict, table: str) -> Dict:
        table = self.dynamodb.Table(table)

        try:
            response = table.get_item(Key=item_id)
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            return response.get("Item")

    def put_item(self, item: Dict, table: str) -> Dict:
        table = self.dynamodb.Table(table)
        response = table.put_item(Item=item)
        return response

    def del_item(self, item: object):
        pass
