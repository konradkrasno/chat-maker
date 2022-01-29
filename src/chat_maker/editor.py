import json
from pathlib import Path
from typing import List

from chat_maker.user_phrase_parser import UserPhraseParserMapping
from chat_maker.exceptions import (
    ParserTypeNotExistsError,
    UserPhraseTypeExistsError,
    NodeNotExistsError,
    NodeExistsError,
    ConfigurationError,
)


class ChatEditor:
    def __init__(self, file_path: str) -> None:
        if file_path:
            self.file_path = file_path
        elif Path("../../.config").exists():
            with open("../../.config", "r") as file:
                lines = file.readlines()
                for line in lines:
                    if "chat_file_path" in line:
                        self.file_path = line.split("=")[1]
        else:
            raise ConfigurationError("Chat editor improperly configured.")

    def load_chat_obj(self) -> json:
        with open(self.file_path, "r") as file:
            return json.load(file)

    def dump_chat_obj(self, _object: json) -> None:
        with open(self.file_path, "w") as file:
            json.dump(_object, file)

    def add_node(self, node_name: str) -> None:
        if not node_name:
            raise ConfigurationError("Node name can not be empty.")

        chat_obj = self.load_chat_obj()

        if node_name in chat_obj["Nodes"]:
            raise NodeExistsError(f"Node with name '{node_name}' already exists.")

        chat_obj["Nodes"][node_name] = {
            "BotPhrases": [],
            "UserPhrases": [],
            "FailPhrases": [],
        }
        self.dump_chat_obj(chat_obj)
        print(f"Successfully created node '{node_name}'.")

    def remove_node(self, node_name: str) -> None:
        if not node_name:
            raise ConfigurationError("Node name can not be empty.")

        chat_obj = self.load_chat_obj()
        try:
            del chat_obj["Nodes"][node_name]
            print(f"Successfully deleted node '{node_name}'.")
        except KeyError:
            print(f"Node with name '{node_name}' does not exist.")
        self.dump_chat_obj(chat_obj)

    def add_bot_phrases(self):
        pass

    def remove_bot_phrases(self):
        pass

    def add_user_phrase(
        self,
        edited_node: str,
        success_node: str,
        user_phrase_type: str,
        user_phrase_items: List = [],
    ) -> None:
        if not edited_node:
            raise ConfigurationError("Edited node name not provided.")
        if not success_node:
            raise ConfigurationError("Success node name not provided.")
        if not user_phrase_type:
            raise ConfigurationError("User phrase type not provided.")

        chat_obj = self.load_chat_obj()
        try:
            user_phrases = chat_obj["Nodes"][edited_node]["UserPhrases"]
        except KeyError:
            raise NodeNotExistsError(
                f"Node with name: '{edited_node}' does not exists. Add new node first."
            )

        if user_phrase_type not in UserPhraseParserMapping.keys():
            raise ParserTypeNotExistsError(
                f"UserPhrase parser type: '{user_phrase_type}' not exists."
            )

        if success_node not in chat_obj["Nodes"].keys():
            raise NodeNotExistsError(
                f"Node with name: '{success_node}' does not exists. Add new node first."
            )

        for phrase in user_phrases:
            if phrase["UserPhraseMatch"]["Type"] == user_phrase_type:
                raise UserPhraseTypeExistsError(
                    f"UserPhrase type '{user_phrase_type}' already exists in node '{edited_node}'"
                )

        new_phrase = {
            "UserPhraseMatch": {"Type": user_phrase_type, "Items": user_phrase_items},
            "SuccessNode": success_node,
        }
        user_phrases.append(new_phrase)
        self.dump_chat_obj(chat_obj)

    def remove_user_phrase(self, edited_node: str, user_phrase_type: str) -> None:
        if not edited_node:
            raise ConfigurationError("Edited node name not provided.")
        if not user_phrase_type:
            raise ConfigurationError("User phrase type not provided.")

        chat_obj = self.load_chat_obj()
        try:
            user_phrases = chat_obj["Nodes"][edited_node]["UserPhrases"]
        except KeyError:
            raise NodeNotExistsError(
                f"Node with name: '{edited_node}' does not exists."
            )

        filtered_phrases = [
            item
            for item in user_phrases
            if item["UserPhraseMatch"]["Type"] != user_phrase_type
        ]
        chat_obj["Nodes"][edited_node]["UserPhrases"] = filtered_phrases
        self.dump_chat_obj(chat_obj)

    def change_success_node(
        self,
        edited_node: str,
        success_node: str,
        user_phrase_type: str,
        user_phrase_items: List = [],
    ) -> None:
        # TODO finish
        pass

    def add_fail_phrases(self):
        pass

    def remove_fail_phrases(self):
        pass