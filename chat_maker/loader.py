import json

from chat_maker.models import Chat
from chat_maker.schemas import ChatSchema
from chat_maker.dynamodb import DynamoDBClient

chat_id_mock = {
    "BC4F3C85D8": "./fixtures/chat_flow.json",
    "local": "./tests/chat_flow.json",
}


class ChatLoader:
    def __init__(
        self, chat_id: str, from_dynamodb: bool = True, aws_region: str = None
    ) -> None:
        self.chat_id = chat_id
        self.aws_region = aws_region
        self.dynamodb_client = (
            DynamoDBClient(aws_region=aws_region) if from_dynamodb else None
        )
        self._chat_data = self._get_chat_data()
        self.chat = self._load_chat()

    def _get_chat_data(self) -> json:
        if self.dynamodb_client:
            chat_item = self.dynamodb_client.get_item(
                {"chat_id": self.chat_id}, "chat-maker-table.chat"
            )
            if chat_item:
                return chat_item
            raise Exception("Chat item is None. Check DynamoDB connection or chat id.")

        file_path = chat_id_mock[self.chat_id]
        with open(file_path, "r") as file:
            return json.load(file)

    def _load_chat(self) -> Chat:
        chat_schema = ChatSchema()
        chat_model = chat_schema.load(self._chat_data)
        return chat_model

    def dump_chat(self) -> None:
        chat_schema = ChatSchema()
        if self.dynamodb_client:
            self.dynamodb_client.put_item(
                chat_schema.dump(self.chat), "chat-maker-table.chat"
            )
        else:
            file_path = chat_id_mock[self.chat_id]
            with open(file_path, "w") as file:
                json.dump(chat_schema.dump(self.chat), file)
