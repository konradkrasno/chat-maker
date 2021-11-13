import sys

from commands import CommandHandler


if __name__ == "__main__":
    args = sys.argv[1:]
    handler = CommandHandler()
    try:
        command = args[0]
    except IndexError:
        print("No command provided.")
        handler.handle_command("help")
    else:
        try:
            handler.handle_command(command, *args[1:])
        except Exception as e:
            print(e)
