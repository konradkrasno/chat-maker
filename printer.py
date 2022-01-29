from typing import List

from pathlib import Path

from loader import ChatLoader
from chat import Chat
from exceptions import ConfigurationError


class Printer:
    def __init__(self, file_path: str = None, chat: Chat = None) -> None:
        if chat:
            self.chat = chat
        elif file_path:
            self.chat = ChatLoader(logic_file_path=file_path)
        elif Path("./.config").exists():
            with open("./.config", "r") as file:
                lines = file.readlines()
                for line in lines:
                    if "chat_file_path" in line:
                        path = line.split("=")[1]
                        self.chat = ChatLoader(logic_file_path=path)
        else:
            raise ConfigurationError("Printer improperly configured.")


class GraphPrinter(Printer):
    def __init__(self, file_path: str = None, chat: Chat = None) -> None:
        super().__init__(file_path, chat)

    def get_success_nodes(self, node_name: str) -> List:
        cur_node = self.chat.nodes[node_name]
        return [nd.success_node for nd in cur_node.user_phrases]

    def extend_level(self, node_name: str, nodes: List) -> List:
        cur_node = self.chat.nodes[node_name]
        next_nodes = [
            nd.success_node
            for nd in cur_node.user_phrases
            if nd.success_node not in nodes
        ]
        nodes.extend(next_nodes)
        return nodes

    @staticmethod
    def get_line_width(item: List) -> int:
        spaces = (len(item) - 1)
        width = spaces
        width += sum((len(word) for word in item))
        return width

    def get_max_width(self, tree: List) -> int:
        max_width = 0
        for item in tree:
            width = self.get_line_width(item)
            if width > max_width:
                max_width = width
        return max_width

    def print_graph(self):
        current_node = self.chat.start_node
        tree = []

        level_nodes = [current_node]
        while True:
            tree.append(level_nodes)
            next_level_nodes = []
            for node in level_nodes:
                next_level_nodes = self.extend_level(node, next_level_nodes)

            if len(next_level_nodes) == 0:
                break

            level_nodes = next_level_nodes

        max_width = self.get_max_width(tree)

        for i, items in enumerate(tree):
            if i > 0:
                pass
                    # print(next_nodes)
                # if len(item) == 1 and len(tree[i-1]) == 1:
                #     whitespaces = " " * (max_width//2)
                #     print(whitespaces, "|")
                # elif len(item) == 2 and len(tree[i-1]) == 1:
                #     whitespaces = " " * (max_width//2 - 1)
                #     print(whitespaces, "/ \\")

            whitespaces = " " * (max_width//2 - self.get_line_width(items)//2)
            # print(whitespaces, *items)

            for item in items:
                next_nodes = self.get_success_nodes(item)
                print(item, next_nodes)
