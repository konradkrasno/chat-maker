import json
from typing import Dict, List

from pytest import fixture

from chat_maker.models import Chat
from chat_maker.loader import ChatLoader
from chat_maker.editor import ChatEditor


@fixture(scope="session")
def chat_id() -> str:
    return "local"


@fixture(scope="session")
def chat(chat_id) -> Chat:
    return ChatLoader(chat_id=chat_id, from_dynamodb=False).chat


@fixture(scope="session")
def user_answers() -> List:
    return ["fine, thanks", "lunch", "4240 Benson Park Drive", ""]


@fixture(scope="session")
def answer_matchers() -> Dict:
    return {
        "Start": {"UserPhrase": "fine, thanks", "Result": "fine, thanks"},
        "Order": {"UserPhrase": "lunch", "Result": "lunch"},
        "ClientAddress": {
            "UserPhrase": "4240 Benson Park Drive",
            "Result": "4240 Benson Park Drive",
        },
    }


@fixture(scope="session")
def editor(chat_id) -> ChatEditor:
    return ChatEditor(chat_id=chat_id, from_dynamodb=False)


@fixture(scope="session")
def test_data() -> json:
    with open("./tests/test_data.json", "r") as file:
        return json.load(file)
