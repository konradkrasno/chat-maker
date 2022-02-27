import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.absolute()
sys.path.append(BASE_DIR.__str__())

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


if __name__ == "__main__":
    main()
