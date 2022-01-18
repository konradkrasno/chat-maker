# chat-maker

### Prepare environment
```
make build
```
### Configuration
```
alias chatmaker="python3 chat_maker.py"

chatmaker config --chat-file-path=./tests/chat_flow.json
```


### Commands
```
chatmaker remove_node --file-path=./tests/chat_flow.json --node-name=TestNode
chatmaker remove_node --file-path=./tests/chat_flow.json --node-name=TestNode
chatmaker add_user_phrase \
    --file-path=./tests/chat_flow.json \
    --edited-node=TestNode \
    --success-node=End \
    --user-phrase-type=ContainsItems \
    --user-phrase-items=test1,test2,test3

chatmaker remove_user_phrase \
    --edited-node=Test \
    --user-phrase-type=Time
```
