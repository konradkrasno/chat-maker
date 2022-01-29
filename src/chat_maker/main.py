import sys

from chat_maker.commands import CommandHandler


def main():
    args = sys.argv[1:]
    try:
        command = args[0]
    except IndexError:
        print("No command provided.")
        CommandHandler.help()
    else:
        handler = CommandHandler(command)
        handler.run_command(*args[1:])
