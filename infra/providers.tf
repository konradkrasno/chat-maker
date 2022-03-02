provider "aws" {
  region = var.region

  dynamic "endpoints" {
    for_each = var.environment == "dev" ? [1] : []
    content {
      dynamodb = "http://localhost:4566"
      lambda   = "http://localhost:4566"
    }
  }
}
