from chat_maker.loader import ChatLoader


if __name__ == "__main__":
    chat = ChatLoader(logic_file_path="../../tests/chat_flow.json")
    chat.run_chat()
