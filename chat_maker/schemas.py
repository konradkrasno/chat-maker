from marshmallow import Schema, fields, post_load

from chat_maker.models import Chat, Node, UserPhrase


class UserPhraseSchema(Schema):
    name = fields.Str()
    success_node = fields.Str()
    match_type = fields.Str()
    items = fields.List(fields.Str())

    @post_load
    def make_user_phrase(self, data, **kwargs):
        return UserPhrase(**data)


class NodeSchema(Schema):
    name = fields.Str()
    bot_phrases = fields.List(fields.Str())
    user_phrases = fields.Dict(
        keys=fields.Str(), values=fields.Nested(UserPhraseSchema())
    )
    fail_phrases = fields.List(fields.Str())

    @post_load
    def make_node(self, data, **kwargs):
        return Node(**data)


class ChatSchema(Schema):
    chat_id = fields.Str()
    name = fields.Str()
    start_node = fields.Str()
    nodes = fields.Dict(keys=fields.Str(), values=fields.Nested(NodeSchema()))

    @post_load
    def make_chat(self, data, **kwargs):
        return Chat(**data)
