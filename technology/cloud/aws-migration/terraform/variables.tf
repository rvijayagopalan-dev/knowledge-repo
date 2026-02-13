variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "microservices-migration"
}

# Networking Variables
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]
}

variable "database_subnet_cidrs" {
  description = "CIDR blocks for database subnets"
  type        = list(string)
  default     = ["10.0.20.0/24", "10.0.21.0/24"]
}

# ECS Variables
variable "ecs_services" {
  description = "Map of ECS services to create"
  type = map(object({
    name              = string
    cpu               = number
    memory            = number
    desired_count     = number
    container_port    = number
    health_check_path = string
  }))
  default = {
    user-service = {
      name              = "user-service"
      cpu               = 512
      memory            = 1024
      desired_count     = 2
      container_port    = 8080
      health_check_path = "/health"
    }
    order-service = {
      name              = "order-service"
      cpu               = 1024
      memory            = 2048
      desired_count     = 2
      container_port    = 8081
      health_check_path = "/health"
    }
  }
}

# RDS Variables
variable "db_engine" {
  description = "Database engine (postgres, mysql)"
  type        = string
  default     = "postgres"
}

variable "db_engine_version" {
  description = "Database engine version"
  type        = string
  default     = "15.4"
}

variable "db_instance_class" {
  description = "RDS instance type"
  type        = string
  default     = "db.t3.medium"
}

variable "db_allocated_storage" {
  description = "Allocated storage in GB"
  type        = number
  default     = 100
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "microservices_db"
}

variable "db_username" {
  description = "Database master username"
  type        = string
  default     = "dbadmin"
}

variable "db_multi_az" {
  description = "Enable Multi-AZ deployment"
  type        = bool
  default     = true
}

# Monitoring Variables
variable "enable_cloudwatch_logs" {
  description = "Enable CloudWatch logs"
  type        = bool
  default     = true
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 30
}

variable "alarm_email" {
  description = "Email address for CloudWatch alarms"
  type        = string
  default     = "alerts@example.com"
}

# API Gateway Variables
variable "enable_api_gateway" {
  description = "Enable API Gateway"
  type        = bool
  default     = true
}

variable "api_gateway_stage" {
  description = "API Gateway stage name"
  type        = string
  default     = "v1"
}

# Tags
variable "additional_tags" {
  description = "Additional tags for resources"
  type        = map(string)
  default     = {}
}
