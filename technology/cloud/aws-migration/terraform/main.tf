# Main Terraform configuration for AWS Microservices Migration

locals {
  common_tags = merge(
    {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    },
    var.additional_tags
  )
}

# Networking Module
module "networking" {
  source = "./modules/networking"

  project_name           = var.project_name
  environment            = var.environment
  vpc_cidr               = var.vpc_cidr
  availability_zones     = var.availability_zones
  public_subnet_cidrs    = var.public_subnet_cidrs
  private_subnet_cidrs   = var.private_subnet_cidrs
  database_subnet_cidrs  = var.database_subnet_cidrs

  tags = local.common_tags
}

# ECS Module
module "ecs" {
  source = "./modules/ecs"

  project_name       = var.project_name
  environment        = var.environment
  vpc_id             = module.networking.vpc_id
  public_subnet_ids  = module.networking.public_subnet_ids
  private_subnet_ids = module.networking.private_subnet_ids
  ecs_services       = var.ecs_services

  tags = local.common_tags

  depends_on = [module.networking]
}

# RDS Module
module "rds" {
  source = "./modules/rds"

  project_name         = var.project_name
  environment          = var.environment
  vpc_id               = module.networking.vpc_id
  database_subnet_ids  = module.networking.database_subnet_ids
  db_engine            = var.db_engine
  db_engine_version    = var.db_engine_version
  db_instance_class    = var.db_instance_class
  db_allocated_storage = var.db_allocated_storage
  db_name              = var.db_name
  db_username          = var.db_username
  db_multi_az          = var.db_multi_az

  # Allow access from ECS tasks
  allowed_security_group_ids = [module.ecs.ecs_task_security_group_id]

  tags = local.common_tags

  depends_on = [module.networking]
}

# API Gateway Module (Optional)
module "api_gateway" {
  count  = var.enable_api_gateway ? 1 : 0
  source = "./modules/api-gateway"

  project_name      = var.project_name
  environment       = var.environment
  vpc_id            = module.networking.vpc_id
  alb_listener_arn  = module.ecs.alb_listener_arn
  alb_dns_name      = module.ecs.alb_dns_name
  stage_name        = var.api_gateway_stage

  tags = local.common_tags

  depends_on = [module.ecs]
}

# Monitoring Module
module "monitoring" {
  source = "./modules/monitoring"

  project_name          = var.project_name
  environment           = var.environment
  ecs_cluster_name      = module.ecs.cluster_name
  ecs_service_names     = [for svc in var.ecs_services : svc.name]
  rds_instance_id       = module.rds.db_instance_id
  alb_arn_suffix        = module.ecs.alb_arn_suffix
  enable_cloudwatch_logs = var.enable_cloudwatch_logs
  log_retention_days    = var.log_retention_days
  alarm_email           = var.alarm_email

  tags = local.common_tags

  depends_on = [module.ecs, module.rds]
}
