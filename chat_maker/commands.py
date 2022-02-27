import argparse
from pathlib import Path
from typing import Dict, Tuple
from json.decoder import JSONDecodeError

from chat_maker.editor import ChatEditor
from chat_maker.printer import GraphPrinter
from chat_maker.exceptions import ConfigurationError


COMMANDS = {
    "help": {
        "description": "Prints available commands with descriptions.",
        "class_args": [],
        "method_args": [],
    },
    "config": {
        "description": "Creates file with chat basic configuration.",
        "class_args": [],
        "method_args": [
            {"name": "--chat-id", "type": str, "description": "Provides chat id."}
        ],
    },
    # "print_graph": {
    #     "description": "Command for printing tree of nodes.",
    #     "class": GraphPrinter,
    #     "class_args": [
    #         {
    #             "name": "--chat-id",
    #             "type": str,
    #             "description": "Provides chat id.",
    #         }
    #     ],
    #     "method_args": [],
    # },
    "create_node": {
        "description": "Command for adding new node.",
        "class": ChatEditor,
        "class_args": [
            {
                "name": "--chat-id",
                "type": str,
                "description": "Provides chat id.",
            },
            {
                "name": "--from-dynamodb",
                "type": bool,
                "description": "Determines if DynamoDb will be using.",
            },
            {
                "name": "--aws-region",
                "type": str,
                "description": "Provides aws region.",
            },
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
            {"name": "--chat-id", "type": str, "description": "Provides chat id."},
            {
                "name": "--from-dynamodb",
                "type": bool,
                "description": "Determines if DynamoDb will be using.",
            },
            {
                "name": "--aws-region",
                "type": str,
                "description": "Provides aws region.",
            },
        ],
        "method_args": [
            {
                "name": "--node-name",
                "type": str,
                "description": "Provides new node name.",
            }
        ],
    },
    "add_user_phrase": {
        "description": "Command for new UserPhrase object.",
        "class": ChatEditor,
        "class_args": [
            {"name": "--chat-id", "type": str, "description": "Provides chat id."},
            {
                "name": "--from-dynamodb",
                "type": bool,
                "description": "Determines if DynamoDb will be using.",
            },
            {
                "name": "--aws-region",
                "type": str,
                "description": "Provides aws region.",
            },
        ],
        "method_args": [
            {
                "name": "--edited-node",
                "type": str,
                "description": "Determines node for editing.",
            },
            {
                "name": "--user-phrase-name",
                "type": str,
                "description": "Determines user phrase name.",
            },
            {
                "name": "--success-node",
                "type": str,
                "description": "Provides name of node which is the next after success in current node.",
            },
            {
                "name": "--user-phrase-type",
                "type": str,
                "description": "Provides type of user phrase.",
            },
            {
                "name": "--user-phrase-items",
                "type": lambda s: s.split(","),
                "description": "Provides list of user phrase items, usage: item1,item2,item3",
            },
        ],
    },
    "remove_user_phrase": {
        "description": "Command for removing UserPhrase object.",
        "class": ChatEditor,
        "class_args": [
            {
                "name": "--chat-id",
                "type": str,
                "description": "Provides chat id.",
            },
            {
                "name": "--from-dynamodb",
                "type": bool,
                "description": "Determines if DynamoDb will be using.",
            },
            {
                "name": "--aws-region",
                "type": str,
                "description": "Provides aws region.",
            },
        ],
        "method_args": [
            {
                "name": "--edited-node",
                "type": str,
                "description": "Determines node for editing.",
            },
            {
                "name": "--user-phrase-name",
                "type": str,
                "description": "Provides type of user phrase name.",
            },
        ],
    },
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
        inst = self.command_data.get("class")
        if inst:
            return inst(**kwargs)
        return self

    def handle_command(self, *args, **kwargs) -> None:
        cls_args = self.parse_args("class_args", args)
        mtd_args = self.parse_args("method_args", args)
        cmd_inst = self.get_mtd_cls_inst(**cls_args.__dict__)
        method = getattr(cmd_inst, self.command_name)
        method(**mtd_args.__dict__)

    def run_command(self, *args, **kwargs) -> None:
        try:
            self.handle_command(self.command_name, *args)
        except JSONDecodeError as e:
            print(f"Input file improperly configured: {e}")
        except ConfigurationError as e:
            print(e.__str__())
            self.print_args_info(self.command_data)
        # except Exception as e:
        #     print(e.__str__())

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

    @classmethod
    def config(cls, *args, **kwargs):
        chat_id = kwargs.get("chat_id")
        if not chat_id:
            raise ConfigurationError("Chat id not provided.")

        Path("../.config").touch(exist_ok=True)
        with open("../.config", "w") as file:
            file.write(f"chat_id={chat_id}")
