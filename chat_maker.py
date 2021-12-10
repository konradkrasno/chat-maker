import sys

from commands import CommandHandler


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        command = args[0]
    except IndexError:
        print("No command provided.")
        CommandHandler.help()
    else:
        handler = CommandHandler(command)
        handler.run_command(command, *args[1:])
