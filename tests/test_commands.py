from unittest.mock import patch, call

from chat_maker.commands import CommandHandler


def test_command_handler(test_data):
    for command, options in test_data.items():
        handler = CommandHandler(command)
        for option in options:
            if "print_calls" in option["result"]:
                with patch("builtins.print") as mocked_print:
                    handler.run_command(*option["class_args"], *option["method_args"])
                    mocked_print.assert_has_calls(
                        [call(c) for c in option["result"]["print_calls"]]
                    )
            if "check_code" in option["result"]:
                handler.run_command(*option["class_args"], *option["method_args"])
                exec(option["result"]["check_code"])
