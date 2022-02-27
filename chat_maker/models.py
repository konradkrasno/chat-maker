from typing import Dict, List
from random import choice

from chat_maker.user_phrase_parser import UserPhraseParserMapping


class UserPhrase:
    def __init__(
        self, name, success_node: str, match_type: str, items: List = None
    ) -> None:
        self.name = name
        self.success_node = success_node
        self.match_type = match_type
        self.items = items if items else list()
        self.match_parser = UserPhraseParserMapping[match_type]

    def __repr__(self):
        return f"<SuccessNode>:{self.success_node}<MathType>:{self.match_type}<Items>{self.items}"


class Node:
    def __init__(
        self,
        name: str,
        bot_phrases: List[str] = None,
        user_phrases: Dict = None,
        fail_phrases: List[str] = None,
    ) -> None:
        self.name = name
        self.bot_phrases = bot_phrases if bot_phrases else list()
        self.user_phrases = user_phrases if user_phrases else dict()
        self.fail_phrases = fail_phrases if fail_phrases else list()

    def __repr__(self):
        return self.name

    def add_user_phrase(self, name: str, phrase: "UserPhrase") -> None:
        self.user_phrases[name] = phrase

    def remove_user_phrase(self, name: str) -> None:
        self.user_phrases.__delitem__(name)

    def add_bot_phrase(self, phrase: str) -> None:
        self.bot_phrases.append(phrase)

    def remove_bot_phrase(self, phrase: str) -> None:
        self.bot_phrases.remove(phrase)

    def add_fail_phrase(self, phrase: str) -> None:
        self.fail_phrases.append(phrase)

    def remove_fail_phrase(self, phrase: str) -> None:
        self.fail_phrases.remove(phrase)

    def match_user_phrase(self, user_response: str) -> Dict:
        for user_phrase in self.user_phrases.values():
            parser = user_phrase.match_parser(user_response)
            result = parser.parse()
            if result:
                return {
                    "result": result,
                    "next_node": user_phrase.success_node,
                }
        return {"result": choice(self.fail_phrases), "next_node": self.name}


class Chat:
    def __init__(self, chat_id: str, name: str, start_node: str, nodes: Dict) -> None:
        self.chat_id = chat_id
        self.name = name
        self.start_node = start_node
        self.current_node_name = start_node
        self.nodes = nodes

    @property
    def current_node(self) -> Node:
        return self.nodes[self.current_node_name]

    def add_node(self, node: Node) -> None:
        self.nodes[node.name] = node

    def del_node(self, node_name: str) -> None:
        del self.nodes[node_name]

    @staticmethod
    def get_bot_phrase(node: Node) -> None:
        print(choice(node.bot_phrases))

    @staticmethod
    def get_user_phrase(node: Node) -> Dict:
        user_phrase = input()
        return node.match_user_phrase(user_response=user_phrase)

    def check_consistence(self):
        # Checks if all nodes have appropriate successors and the last node is End node.
        # TODO finish
        pass

    def run_chat(self):
        while True:
            self.get_bot_phrase(self.current_node)
            response = self.get_user_phrase(self.current_node)

            result = response["result"]
            next_node_name = response["next_node"]

            print("result:", result)
            print("next_node:", next_node_name)

            if self.current_node.name == "End":
                break

            self.current_node_name = next_node_name
