import json
import uuid

from typing import Dict
from chat_maker.dynamodb import DynamoDBClient
from chat_maker.exceptions import ConfigurationError


class Initializer:
    def __init__(self, from_dynamodb: bool = True, aws_region: str = None):
        self.aws_region = aws_region
        self.dynamodb_client = (
            DynamoDBClient(aws_region=aws_region) if from_dynamodb else None
        )

    def init_chat(self, chat_name: str) -> Dict:
        if not chat_name:
            raise ConfigurationError("Chat name not provided.")

        chat_id = uuid.uuid4().hex[:10].upper()
        print("chat_id:", chat_id)
        chat_template = {
            "name": chat_name,
            "start_node": "Start",
            "chat_id": chat_id,
            "nodes": {
                "End": {
                    "name": "End",
                    "user_phrases": {},
                    "bot_phrases": [],
                    "fail_phrases": [],
                }
            },
        }

        if self.dynamodb_client:
            self.dynamodb_client.put_item(chat_template, "chat-maker-table.chat")
        else:
            with open(f"{chat_name}.json", "w") as file:
                json.dump(chat_template, file)
        return {"chat_name": chat_name, "chat_id": chat_id}
