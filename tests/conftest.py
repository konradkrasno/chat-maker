import json
from typing import Dict, List

import pytest
from loader import ChatLoader
from editor import ChatEditor
from pytest import fixture


@fixture(scope="session")
def chat_flow_file_path() -> str:
    return "./tests/chat_flow.json"


@pytest.fixture(scope="session")
def chat_obj(chat_flow_file_path) -> json:
    with open(chat_flow_file_path, "r") as file:
        return json.load(file)


@fixture(scope="session")
def chat(chat_flow_file_path) -> ChatLoader:
    return ChatLoader(logic_file_path=chat_flow_file_path)


@fixture(scope="session")
def user_answers() -> List:
    return [
        "fine, thanks",
        "lunch",
        "4240 Benson Park Drive",
        ""
    ]


@fixture(scope="session")
def answer_matchers() -> Dict:
    return {
        "Start": {
            "UserPhrase": "fine, thanks",
            "Result": "fine, thanks"
        },
        "Order": {
            "UserPhrase": "lunch",
            "Result": "lunch"            
        },
        "ClientAddress": {
            "UserPhrase": "4240 Benson Park Drive",
            "Result": "4240 Benson Park Drive"
        },
    }


@fixture(scope="session")
def editor(chat_flow_file_path) -> ChatEditor:
    return ChatEditor(file_path=chat_flow_file_path)
