import argparse

from editor import ChatEditor
from printer import Printer
from exceptions import ConfigurationError

from typing import Dict, Tuple


COMMANDS = {
    "print_graph": {
        "description": "Command for printing tree of nodes.",
        "class": Printer,
        "class_args": [
            {
                "name": "--file-path",
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
                "name": "--file-path",
                "type": str,
                "description": "Provides path to file to be edited.",
            }
        ],
        "method_args": [
            {
                "name": "--node-name",
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
                "name": "--file-path",
                "type": str,
                "description": "Provides path to file to be edited.",
            }
        ],
        "method_args": [
            {
                "name": "--node-name",
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
                "name": "--file-path",
                "type": str,
                "description": "Provides path to file to be edited.",
            }
        ],
        "method_args": [
            {
                "name": "--edited-node",
                "type": str,
                "description": "Determines node for editing.",
            },
            {
                "name": "--success-node",
                "type": str,
                "description": "???",
            },
                        {
                "name": "--user-phrase-type",
                "type": str,
                "description": "???",
            },
                        {
                "name": "--user-phrase-items",
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
    def __init__(self, command_name: str):
        self.command_name = command_name

    @property
    def command_data(self) -> Dict:
        try:
            return COMMANDS[self.command_name]
        except KeyError:
            print(f"Command with name '{self.command_name}' does not exist.")
            exit(1)

    def parse_args(self, group: str, args: Tuple) -> argparse.Namespace:
        parser = argparse.ArgumentParser()
        fltr_args = []
        for cmd in self.command_data[group]:
            parser.add_argument(cmd["name"], type=cmd["type"], help=cmd["description"])
            for arg in args:
                if arg.startswith(cmd["name"]):
                    fltr_args.append(arg)
        return parser.parse_args(fltr_args)

    def get_mtd_cls_inst(self, **kwargs):
        try:
            return self.command_data["class"](**kwargs)
        except KeyError:
            return self
        except ConfigurationError as e:
            print(e)
            self.print_args_info(self.command_data)
            exit(1)

    def handle_command(self, *args, **kwargs) -> None:
        cls_args = self.parse_args("class_args", args)
        mtd_args = self.parse_args("method_args", args)
        cmd_inst = self.get_mtd_cls_inst(**cls_args.__dict__)
        method = getattr(cmd_inst, self.command_name)
        method(**mtd_args.__dict__)

    def run_command(self, command_name: str, *args, **kwargs) -> None:
        try:
            self.handle_command(command_name, *args)
        except Exception as e:
            print(e)

    @staticmethod
    def print_args_info(cmd_data: Dict) -> None:
        for arg in cmd_data["class_args"]:
            print(f"      {arg['name']}")
            print(f"        {arg['description']}")
        for arg in cmd_data["method_args"]:
            print(f"      {arg['name']}")
            print(f"        {arg['description']}")

    @classmethod
    def help(cls, *args, **kwargs) -> None:
        print("Available commands:")
        for cmd, data in COMMANDS.items():
            print(f"  {cmd}")
            print(f"    {data['description']}")
            print(f"    arguments:")
            cls.print_args_info(data)
