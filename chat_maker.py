from commands import CommandHandler
import sys


if __name__ == "__main__":
    args = sys.argv[1:]
    handler = CommandHandler()
    try:
        method = getattr(handler, args[0])
        method(*args[1:])
    except IndexError:
        print("No command provided.")
        handler.help()
    except AttributeError:
        print(f"No command '{args[0]}' available")
