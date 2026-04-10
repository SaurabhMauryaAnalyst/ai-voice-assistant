
variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "voice-cluster"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prod"
}

variable "node_instance_type" {
  description = "EC2 instance type for worker nodes"
  type        = string
  default     = "t3.micro"   # 2 vCPU, 4GB RAM — good for voice workloads
}