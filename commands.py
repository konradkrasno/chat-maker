import argparse
import re

from editor import ChatEditor
from printer import Printer
from exceptions import CommandNotExistsError

from typing import Dict, List


COMMANDS = {
    "print_graph": {
        "description": "Command for printing tree of nodes.",
        "class": Printer,
        "class_args": [
            {
                "name": "--file_path",
                "type": str,
                "description": "Provides path for chat logic json file.",
            }
        ],
        "method_args": [],
    },
    "add_node": {
        "description": "Command for adding new node.",
        "class": ChatEditor,
        "class_args": [
            {
                "name": "--file_path",
                "type": str,
                "description": "Provides path to file to be edited.",
            }
        ],
        "method_args": [
            {
                "name": "--node_name",
                "type": str,
                "description": "Provides new node name.",
            }
        ],
    },
    "remove_node": {
        "description": "Command for deleting node.",
        "class": ChatEditor,
        "class_args": [
            {
                "name": "--file_path",
                "type": str,
                "description": "Provides path to file to be edited.",
            }
        ],
        "method_args": [
            {
                "name": "--node_name",
                "type": str,
                "description": "Provides new node name.",
            }
        ],
    },
    "help": {
        "description": "Prints available commands with descriptions.",
        "class_args": [],
        "method_args": [],
    },
    "add_user_phrase": {
        "description": "Command for new UserPhrase object.",
        "class": ChatEditor,
        "class_args": [
            {
                "name": "--file_path",
                "type": str,
                "description": "Provides path to file to be edited.",
            }
        ],
        "method_args": [
            {
                "name": "--edited_node",
                "type": str,
                "description": "Determines node for editing.",
            },
            {
                "name": "--success_node",
                "type": str,
                "description": "???",
            },
                        {
                "name": "--user_phrase_type",
                "type": str,
                "description": "???",
            },
                        {
                "name": "--user_phrase_items",
                "type": lambda s: s.split(","),
                "description": "???",
            }
        ],
    },
    # "remove_user_phrase": {
    #     "description": "Command for removing UserPhrase object."
    # },
    # "change_success_node": {
    #     "description": ""
    # }
}


class CommandHandler:
    def parse_args(self, cmd_data: Dict, group: str, args: List) -> argparse.Namespace:
        parser = argparse.ArgumentParser()
        fltr_args = []
        for cmd in cmd_data[group]:
            parser.add_argument(cmd["name"], type=cmd["type"], help=cmd["description"])
            for arg in args:
                if arg.startswith(cmd["name"]):
                    fltr_args.append(arg)
        return parser.parse_args(fltr_args)

    @staticmethod
    def get_command_data(command_name: str) -> Dict:
        try:
            return COMMANDS[command_name]
        except KeyError:
            raise CommandNotExistsError(
                f"Command with name '{command_name}' does not exist."
            )

    @classmethod
    def get_method_class(cls, cmd_data: Dict):
        try:
            return cmd_data["class"]
        except KeyError:
            return cls

    def handle_command(self, command_name: str, *args, **kwargs) -> None:
        cmd_data = self.get_command_data(command_name)
        cls_args = self.parse_args(cmd_data, "class_args", args)
        mtd_args = self.parse_args(cmd_data, "method_args", args)
        cmd_inst = self.get_method_class(cmd_data)(**cls_args.__dict__)
        method = getattr(cmd_inst, command_name)
        method(**mtd_args.__dict__)

    @staticmethod
    def help(*args, **kwargs) -> None:
        # TODO finish
        print("help")
