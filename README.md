# chat-maker

## Commands
python3 chat_maker.py remove_node --file_path=./tests/chat_flow.json --node_name=TestNode
python3 chat_maker.py remove_node --file_path=./tests/chat_flow.json --node_name=TestNode
python3 chat_maker.py add_user_phrase \
    --file_path=./tests/chat_flow.json \
    --edited_node=TestNode \
    --success_node=End \
    --user_phrase_type=ContainsItems \
    --user_phrase_items=test1,test2,test3
