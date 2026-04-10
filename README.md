AI Voice Assistant – DevOps Project

This project demonstrates a production-style cloud-native AI Voice Assistant platform deployed on AWS using modern DevOps tools and infrastructure automation.

The system processes voice input from users, converts speech to text, generates AI responses, and returns synthesized speech through a scalable microservices architecture running on Kubernetes.

The infrastructure is fully automated using Terraform and deployed on Amazon EKS with containerized services.

Architecture

The system follows a cloud-native architecture:

User Browser
      ↓
AWS Application Load Balancer (ALB)
      ↓
Kubernetes Ingress Controller
      ↓
Frontend (React + Nginx)
      ↓
Backend (FastAPI AI Service)
      ↓
Redis (Session & Conversation Storage)
Tech Stack

Cloud

AWS EKS (Kubernetes)
AWS VPC
AWS ECR
AWS ALB
AWS IAM

DevOps

Terraform (Infrastructure as Code)
Docker (Containerization)
Kubernetes (Container Orchestration)
Helm (optional extension)
kubectl / eksctl

Backend

Python
FastAPI
Redis
WebSockets

Frontend

React
Nginx
Web Audio API
Key Features
Infrastructure fully provisioned using Terraform
Containerized microservices using Docker
Kubernetes orchestration with Amazon EKS
ALB Ingress Controller for external traffic routing
Redis for session and conversation history
WebSocket streaming for real-time voice interaction
Horizontal Pod Autoscaling support
Production-style cloud architecture
Project Structure
ai-voice-assistant
│
├── backend/        # FastAPI backend services
├── frontend/       # React voice interface
├── terraform/      # AWS infrastructure (VPC, EKS, ECR)
├── k8s/            # Kubernetes manifests
├── docker-compose.yml
└── README.md
Infrastructure Provisioning

Deploy AWS infrastructure using Terraform:

terraform init
terraform apply

This creates:

VPC
Subnets
EKS Cluster
Node Groups
ECR Repositories
Kubernetes Deployment

Deploy the application:

kubectl apply -f k8s/

This creates:

Backend deployment
Frontend deployment
Redis deployment
Services
Ingress
Autoscaling policies
Learning Outcomes
