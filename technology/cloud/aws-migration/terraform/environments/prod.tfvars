# Production Environment Configuration

aws_region   = "us-east-1"
environment  = "production"
project_name = "microservices-migration"

# Networking
vpc_cidr = "10.0.0.0/16"
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
public_subnet_cidrs   = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
private_subnet_cidrs  = ["10.0.10.0/24", "10.0.11.0/24", "10.0.12.0/24"]
database_subnet_cidrs = ["10.0.20.0/24", "10.0.21.0/24", "10.0.22.0/24"]

# ECS Services
ecs_services = {
  user-service = {
    name              = "user-service"
    cpu               = 1024
    memory            = 2048
    desired_count     = 3
    container_port    = 8080
    health_check_path = "/health"
  }
  order-service = {
    name              = "order-service"
    cpu               = 1024
    memory            = 2048
    desired_count     = 3
    container_port    = 8081
    health_check_path = "/health"
  }
}

# RDS
db_engine            = "postgres"
db_engine_version    = "15.4"
db_instance_class    = "db.r6g.large"
db_allocated_storage = 200
db_name              = "production_db"
db_username          = "dbadmin"
db_multi_az          = true

# Monitoring
enable_cloudwatch_logs = true
log_retention_days     = 90
alarm_email            = "production-alerts@example.com"

# API Gateway
enable_api_gateway = true
api_gateway_stage  = "v1"

# Tags
additional_tags = {
  CostCenter = "Engineering"
  Compliance = "SOC2"
}
