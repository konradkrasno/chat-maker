resource "aws_dynamodb_table" "chat_table" {
  name           = "chat-maker-table.chat"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "ChatId"

  attribute {
    name = "ChatId"
    type = "S"
  }

  tags = {
    Name        = "chat-maker-table.chat"
    Environment = "dev"
  }
}
