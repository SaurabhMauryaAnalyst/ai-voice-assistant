terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }

  # Remote state — Terraform's "memory" stored in S3
  # Change bucket name to your unique bucket (created in Step 3)
  backend "s3" {
    bucket         = "voice-assistant-tfstate-966725471159"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tfstate-lock"   # prevents concurrent applies
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
}