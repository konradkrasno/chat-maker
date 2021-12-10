# chat-maker

### Prepare environment
```
make build
```

### Commands
```
python3 chat_maker.py remove_node --file-path=./tests/chat_flow.json --node-name=TestNode
python3 chat_maker.py remove_node --file-path=./tests/chat_flow.json --node-name=TestNode
python3 chat_maker.py add_user_phrase \
    --file-path=./tests/chat_flow.json \
    --edited-node=TestNode \
    --success-node=End \
    --user-phrase-type=ContainsItems \
    --user-phrase-items=test1,test2,test3

```
