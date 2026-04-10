# Subnet group — tells ElastiCache which private subnets to use
resource "aws_elasticache_subnet_group" "redis" {
  name       = "voice-redis-subnet-group"
  subnet_ids = module.vpc.private_subnets   # private — not accessible from internet
}

# Security group — only allows connections from EKS nodes on port 6379
resource "aws_security_group" "redis" {
  name   = "voice-redis-sg"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = [module.vpc.vpc_cidr_block]  # only from within the VPC
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "voice-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"   # 0.5GB RAM — plenty for session data
  num_cache_nodes      = 1                  # single node (add replication for HA)
  parameter_group_name = "default.redis7"
  engine_version       = "7.0"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.redis.name
  security_group_ids   = [aws_security_group.redis.id]

  tags = { Project = "voice-assistant" }
}

output "redis_endpoint" {
  value = aws_elasticache_cluster.redis.cache_nodes[0].address
  # Format: voice-redis.xxxxx.cfg.use1.cache.amazonaws.com
  # Use this in k8s/configmap.yaml as the REDIS_URL
}