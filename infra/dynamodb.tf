resource "aws_dynamodb_table" "chat_table" {
  name         = "chat-maker-table.chat"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "chat_id"

  attribute {
    name = "chat_id"
    type = "S"
  }

  tags = {
    Name        = "chat-maker-table.chat"
    Environment = "dev"
  }
}
