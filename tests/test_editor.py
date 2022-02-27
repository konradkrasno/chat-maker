import pytest
from unittest import mock
from chat_maker.exceptions import (
    NodeNotExistsError,
    NodeExistsError,
    ParserTypeNotExistsError,
)


def test_create_node_with_node_exists_error(editor):
    with pytest.raises(NodeExistsError):
        editor.create_node("Order")


def test_create_node(editor):
    with mock.patch("chat_maker.editor.ChatEditor.dump_chat") as mocked_dump:
        editor.create_node("new_node")
        assert "new_node" in editor.chat.nodes


def test_remove_node(editor):
    pass


def test_add_user_phrase_with_node_not_exists_exception(editor):
    with pytest.raises(NodeNotExistsError):
        editor.add_user_phrase(
            user_phrase_name="Test",
            edited_node="NotExists",
            success_node="End",
            user_phrase_type="Time",
            user_phrase_items=[],
        )

    with pytest.raises(NodeNotExistsError):
        editor.add_user_phrase(
            user_phrase_name="Test",
            edited_node="Order",
            success_node="NotExists",
            user_phrase_type="Time",
            user_phrase_items=[],
        )


def test_add_user_phrase_with_parser_type_not_exists_exception(editor):
    with pytest.raises(ParserTypeNotExistsError):
        editor.add_user_phrase(
            user_phrase_name="Test",
            edited_node="Order",
            success_node="End",
            user_phrase_type="NotExists",
            user_phrase_items=[],
        )


def test_add_user_phrase_with_success(editor):
    user_phrase_name = "Test"
    edited_node = "Order"
    success_node = "End"
    user_phrase_type = "Time"
    user_phrase_items = []

    with mock.patch("chat_maker.editor.ChatEditor.dump_chat") as mocked_dump:
        editor.add_user_phrase(
            edited_node=edited_node,
            user_phrase_name=user_phrase_name,
            success_node=success_node,
            user_phrase_type=user_phrase_type,
            user_phrase_items=user_phrase_items,
        )
        assert user_phrase_name in editor.chat.nodes[edited_node].user_phrases
