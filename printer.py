from chat import Chat


class Printer:
    def __init__(self, chat: Chat) -> None:
        self.chat = chat
    
    def print_graph(self):
        current_node = "Start"
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
