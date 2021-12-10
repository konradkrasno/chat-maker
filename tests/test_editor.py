import pytest
from unittest import mock
from exceptions import (
    UserPhraseTypeExistsError,
    NodeNotExistsError,
    NodeExistsError,
    ParserTypeNotExistsError,
)


def test_add_node_with_node_exists_error(editor):
    with pytest.raises(NodeExistsError):
        editor.add_node("Order")


def test_add_node(editor):
    with mock.patch("editor.ChatEditor.dump_chat_obj") as mocked_dump:
        editor.add_node("new_node")
        result = mocked_dump.call_args.args[0]
        assert "new_node" in result["Nodes"]


def test_remove_node(editor):
    pass


def test_add_user_phrase_with_user_phrase_type_exists_exception(editor):
    with pytest.raises(UserPhraseTypeExistsError):
        editor.add_user_phrase(
            edited_node="Order",
            success_node="End",
            user_phrase_type="SearchItem",
        )


def test_add_user_phrase_with_node_not_exists_exception(editor):
    with pytest.raises(NodeNotExistsError):
        editor.add_user_phrase(
            edited_node="NotExists",
            success_node="End",
            user_phrase_type="Time",
        )

    with pytest.raises(NodeNotExistsError):
        editor.add_user_phrase(
            edited_node="Order", success_node="NotExists", user_phrase_type="Time"
        )


def test_add_user_phrase_with_parser_type_not_exists_exception(editor):
    with pytest.raises(ParserTypeNotExistsError):
        editor.add_user_phrase(
            edited_node="Order",
            success_node="End",
            user_phrase_type="NotExists",
        )


def test_add_user_phrase_with_success(editor):
    edited_node = "Order"
    success_node = "End"
    user_phrase_type = "Time"

    with mock.patch("editor.ChatEditor.dump_chat_obj") as mocked_dump:
        editor.add_user_phrase(edited_node, success_node, user_phrase_type)
        result = mocked_dump.call_args.args[0]
        for phrase in result["Nodes"][edited_node]["UserPhrases"]:
            if (
                phrase["UserPhraseMatch"]["Type"] == user_phrase_type
                and phrase["SuccessNode"] == success_node
            ):
                return True
    raise Exception("An error occured while adding data to user phrase")
