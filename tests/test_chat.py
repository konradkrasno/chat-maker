from unittest import mock


def test_chat_flow(chat, user_answers):
    with mock.patch("builtins.input", side_effect=user_answers):
        chat.run_chat()


def test_user_phrase_parser(chat, answer_matchers):
    for node_name, answer in answer_matchers.items():
        node = chat.nodes[node_name]
        result = node.match_user_phrase(answer["UserPhrase"])
        assert result["result"] == answer["Result"]
