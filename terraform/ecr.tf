
resource "aws_ecr_repository" "frontend" {
  name                 = "voice-frontend"
  image_tag_mutability = "IMMUTABLE"   # once pushed, a tag can't be overwritten
                                       # prevents accidental overwrites in production

  image_scanning_configuration {
    scan_on_push = true   # automatically scans for CVEs on every docker push
  }

  tags = { Project = "voice-assistant" }
}

resource "aws_ecr_repository" "backend" {
  name                 = "voice-backend"
  image_tag_mutability = "IMMUTABLE"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = { Project = "voice-assistant" }
}

# Lifecycle policy: automatically delete untagged images older than 7 days
# Prevents ECR storage costs from accumulating with old build artifacts
resource "aws_ecr_lifecycle_policy" "backend_cleanup" {
  repository = aws_ecr_repository.backend.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Remove untagged images after 7 days"
      selection = {
        tagStatus   = "untagged"
        countType   = "sinceImagePushed"
        countUnit   = "days"
        countNumber = 7
      }
      action = { type = "expire" }
    }]
  })
}

# Output the ECR URLs so you can use them in Phase 3 (docker push)
output "ecr_frontend_url" {
  value = aws_ecr_repository.frontend.repository_url
}
output "ecr_backend_url" {
  value = aws_ecr_repository.backend.repository_url
}