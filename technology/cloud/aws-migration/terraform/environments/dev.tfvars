# Development Environment Configuration

aws_region   = "us-east-1"
environment  = "development"
project_name = "microservices-migration"

# Networking
vpc_cidr = "10.1.0.0/16"
availability_zones = ["us-east-1a", "us-east-1b"]
public_subnet_cidrs   = ["10.1.1.0/24", "10.1.2.0/24"]
private_subnet_cidrs  = ["10.1.10.0/24", "10.1.11.0/24"]
database_subnet_cidrs = ["10.1.20.0/24", "10.1.21.0/24"]

# ECS Services
ecs_services = {
  user-service = {
    name              = "user-service"
    cpu               = 256
    memory            = 512
    desired_count     = 1
    container_port    = 8080
    health_check_path = "/health"
  }
  order-service = {
    name              = "order-service"
    cpu               = 256
    memory            = 512
    desired_count     = 1
    container_port    = 8081
    health_check_path = "/health"
  }
}

# RDS
db_engine            = "postgres"
db_engine_version    = "15.4"
db_instance_class    = "db.t3.micro"
db_allocated_storage = 20
db_name              = "dev_db"
db_username          = "dbadmin"
db_multi_az          = false

# Monitoring
enable_cloudwatch_logs = true
log_retention_days     = 7
alarm_email            = "dev-alerts@example.com"

# API Gateway
enable_api_gateway = true
api_gateway_stage  = "dev"

# Tags
additional_tags = {
  CostCenter = "Engineering"
  Purpose    = "Development"
}
