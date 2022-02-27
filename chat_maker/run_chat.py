from chat_maker.loader import ChatLoader


if __name__ == "__main__":
    loader = ChatLoader(chat_id="local")
    loader.chat.run_chat()
