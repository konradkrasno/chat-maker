import json
from typing import List

from chat_maker.chat import Chat, Node, UserPhrase


class ChatLoader(Chat):
    def __init__(self, logic_file_path: str) -> None:
        self.logic_file_path = logic_file_path
        super().__init__(
            name=self.logic["ChatName"], start_node=self.logic["StartNode"]
        )
        self._load_chat()

    @property
    def logic(self) -> json:
        with open(self.logic_file_path, "r") as file:
            return json.load(file)

    @staticmethod
    def _get_user_phrases(user_phrases: List) -> List:
        return [
            UserPhrase(
                success_node=user_phrase["SuccessNode"],
                match_type=user_phrase["UserPhraseMatch"]["Type"],
                items=user_phrase["UserPhraseMatch"].get("Items", []),
            )
            for user_phrase in user_phrases
        ]

    def _load_chat(self) -> None:
        for key, val in self.logic.get("Nodes", {}).items():
            user_phrases = self._get_user_phrases(val.get("UserPhrases", []))
            node = Node(
                name=key,
                bot_phrases=val["BotPhrases"],
                user_phrases=user_phrases,
                fail_phrases=val.get("FailPhrases", [""]),
            )
            self.add_node(node)

    def dump_chat(self, dump_file_path: str) -> None:
        pass
