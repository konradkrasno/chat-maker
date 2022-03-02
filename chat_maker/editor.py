from pathlib import Path
from typing import List

from chat_maker.models import Node, UserPhrase
from chat_maker.loader import ChatLoader
from chat_maker.user_phrase_parser import UserPhraseParserMapping
from chat_maker.exceptions import (
    ParserTypeNotExistsError,
    NodeNotExistsError,
    NodeExistsError,
    ConfigurationError,
)


class ChatEditor(ChatLoader):
    def __init__(
        self, chat_id: str, from_dynamodb: bool = True, aws_region: str = None
    ) -> None:
        super().__init__(
            chat_id=chat_id, from_dynamodb=from_dynamodb, aws_region=aws_region
        )

        if chat_id:
            self.chat_id = chat_id
        elif Path(".config").exists():
            with open(".config", "r") as file:
                lines = file.readlines()
                for line in lines:
                    if "chat_id" in line:
                        self.chat_id = line.split("=")[1].replace("\n", "")
        else:
            raise ConfigurationError("Chat editor improperly configured.")

    def create_node(self, node_name: str) -> None:
        if not node_name:
            raise ConfigurationError("Node name can not be empty.")

        if node_name in self.chat.nodes:
            raise NodeExistsError(f"Node with name '{node_name}' already exists.")

        self.chat.add_node(Node(name=node_name))
        self.dump_chat()
        print(f"Successfully created node '{node_name}'.")

    def remove_node(self, node_name: str) -> None:
        if not node_name:
            raise ConfigurationError("Node name can not be empty.")

        try:
            self.chat.del_node(node_name)
            print(f"Successfully deleted node '{node_name}'.")
        except KeyError:
            print(f"Node with name '{node_name}' does not exist.")
        self.dump_chat()

    def add_bot_phrases(self):
        pass

    def remove_bot_phrases(self):
        pass

    def add_user_phrase(
        self,
        edited_node: str,
        user_phrase_name: str,
        success_node: str,
        user_phrase_type: str,
        user_phrase_items: List,
    ) -> None:
        if not edited_node:
            raise ConfigurationError("Edited node name not provided.")
        if not user_phrase_name:
            raise ConfigurationError("User phrase name not provided.")
        if not success_node:
            raise ConfigurationError("Success node name not provided.")
        if not user_phrase_type:
            raise ConfigurationError("User phrase type not provided.")

        try:
            node = self.chat.nodes[edited_node]
        except KeyError:
            raise NodeNotExistsError(
                f"Node with name: '{edited_node}' does not exists. Add new node first."
            )

        if user_phrase_name in node.user_phrases.keys():
            print(f"User phrase with name '{user_phrase_name}' already exists.")
            return None

        if user_phrase_type not in UserPhraseParserMapping.keys():
            raise ParserTypeNotExistsError(
                f"User phrase parser type: '{user_phrase_type}' not exists. "
                f"Available types: {UserPhraseParserMapping.keys()}"
            )

        if success_node not in self.chat.nodes.keys():
            raise NodeNotExistsError(
                f"Node with name: '{success_node}' does not exists. Add new node first."
            )

        new_phrase = UserPhrase(
            name=user_phrase_name,
            success_node=success_node,
            match_type=user_phrase_type,
            items=user_phrase_items if user_phrase_items else [],
        )
        node.add_user_phrase(user_phrase_name, new_phrase)
        print(
            f"User phrase type '{user_phrase_type}' and success node '{success_node}' "
            f"added to node '{edited_node}' successfully."
        )
        self.dump_chat()

    def remove_user_phrase(self, edited_node: str, user_phrase_name: str) -> None:
        if not edited_node:
            raise ConfigurationError("Edited node name not provided.")
        if not user_phrase_name:
            raise ConfigurationError("User phrase name not provided.")

        try:
            node = self.chat.nodes[edited_node]
        except KeyError:
            raise NodeNotExistsError(
                f"Node with name: '{edited_node}' does not exists."
            )

        try:
            node.remove_user_phrase(user_phrase_name)
        except KeyError:
            print(f"User phrase with name '{user_phrase_name}' not exists.")
        else:
            print(f"User phrase '{user_phrase_name}' deleted successfully.")
            self.dump_chat()

    def change_success_node(
        self,
        edited_node: str,
        success_node: str,
        user_phrase_type: str,
        user_phrase_items: List,
    ) -> None:
        # TODO finish
        pass

    def add_fail_phrases(self):
        pass

    def remove_fail_phrases(self):
        pass
