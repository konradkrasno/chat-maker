#!/bin/bash

cat ./tests/chat_flow.json | jq > /tmp/pretty.json
mv /tmp/pretty.json ./tests/chat_flow.json
