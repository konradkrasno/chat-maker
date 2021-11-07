import argparse
import inspect
from printer import Printer
from loader import ChatLoader


COMMANDS = {
    "print_graph": {
        "description": "Command for printing tree of nodes.",
        "args": [
            {
                "name": "--logic_file_path",
                "type": str,
                "description": "Provided path for chat logic json file.",
            }
        ],
    },
    # "add_success_node": {
    #     "description": "Command for adding success node to existing UserPhrase object."
    # },
    # "remove_success_node": {
    #     "description": "Command for remobing success node from existing UserPhrase object."
    # },
    # "help": {
    #     "description": "Prints available commands with descriptions."
    # }
}


class CommandHandler:
    def parse_args(self, command: str, args):
        parser = argparse.ArgumentParser()
        for arg in COMMANDS[command]["args"]:
            parser.add_argument(arg["name"], type=arg["type"], help=arg["description"])
        return parser.parse_args(args)

    @staticmethod
    def help(*args, **kwargs):
        # TODO finish
        print("help")

    def print_graph(self, *args, **kwargs):
        parsed_args = self.parse_args("print_graph", args)
        chat = ChatLoader(logic_file_path=parsed_args.logic_file_path)
        printer = Printer(chat)
        printer.print_graph()

    def add_success_node(self, args, **kwargs):
        # TODO finish
        pass

    def remove_success_node(self, *args, **kwargs):
        # TODO finish
        pass
