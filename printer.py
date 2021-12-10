from loader import ChatLoader
from chat import Chat
from exceptions import ConfigurationError


class Printer:
    def __init__(self, file_path: str = None, chat: Chat = None) -> None:
        if file_path:
            self.chat = ChatLoader(logic_file_path=file_path)
        elif chat:
            self.chat = chat
        else:
            raise ConfigurationError("Printer improperly configured.")

    def print_graph(self):
        current_node = self.chat.start_node
        prefix_count = 0

        print(current_node)
        while True:
            if current_node == "End":
                break

            prefix_count += len(current_node)//2

            node = self.chat.nodes[current_node]
            next_nodes = [phrase.success_node for phrase in node.user_phrases]
            # TODO figure out how to print tree
            current_node = next_nodes[0]

            print("{}\\".format(" " * prefix_count))
            print("{}{}".format(" " * prefix_count, current_node))
