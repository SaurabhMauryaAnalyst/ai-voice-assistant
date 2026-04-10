
# Uses the community VPC module — saves ~200 lines of boilerplate
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.8.0"

  name = "voice-assistant-vpc"
  cidr = "10.0.0.0/16"   # 65,536 private IP addresses available

  # 3 Availability Zones for high availability
  azs = ["us-east-1a", "us-east-1b", "us-east-1c"]

  # Private subnets — EKS nodes and Redis live here
  # Not reachable from internet directly
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]

  # Public subnets — Load Balancer lives here
  # Has direct internet access
  public_subnets = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  # NAT Gateway: lets private subnet resources (pods, Redis)
  # initiate outbound internet connections (e.g. pull Docker images, call APIs)
  # without being reachable FROM the internet
  enable_nat_gateway = true
  single_nat_gateway = true      # One NAT per AZ = HA. Set true to save $65/mo in dev
  

  enable_dns_hostnames = true     # Required for EKS
  enable_dns_support   = true

  # These tags are REQUIRED for EKS to find the right subnets for nodes and load balancers
  private_subnet_tags = {
    "kubernetes.io/cluster/voice-cluster" = "shared"
    "kubernetes.io/role/internal-elb"     = "1"       # internal load balancers go here
  }

  public_subnet_tags = {
    "kubernetes.io/cluster/voice-cluster" = "shared"
    "kubernetes.io/role/elb"              = "1"       # internet-facing ALBs go here
  }

  tags = {
    Environment = "prod"
    Project     = "voice-assistant"
  }
}