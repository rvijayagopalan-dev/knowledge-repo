output "vpc_id" {
  description = "ID of the VPC"
  value       = module.networking.vpc_id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = module.networking.public_subnet_ids
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = module.networking.private_subnet_ids
}

output "ecs_cluster_id" {
  description = "ID of the ECS cluster"
  value       = module.ecs.cluster_id
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = module.ecs.cluster_name
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = module.ecs.alb_dns_name
}

output "alb_zone_id" {
  description = "Zone ID of the Application Load Balancer"
  value       = module.ecs.alb_zone_id
}

output "ecr_repository_urls" {
  description = "URLs of ECR repositories"
  value       = module.ecs.ecr_repository_urls
}

output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = module.rds.db_endpoint
  sensitive   = true
}

output "rds_port" {
  description = "RDS instance port"
  value       = module.rds.db_port
}

output "rds_database_name" {
  description = "RDS database name"
  value       = module.rds.db_name
}

output "api_gateway_url" {
  description = "API Gateway invoke URL"
  value       = var.enable_api_gateway ? module.api_gateway[0].api_url : null
}

output "api_gateway_id" {
  description = "API Gateway ID"
  value       = var.enable_api_gateway ? module.api_gateway[0].api_id : null
}

output "cloudwatch_log_groups" {
  description = "CloudWatch log group names"
  value       = module.monitoring.log_group_names
}

output "sns_topic_arn" {
  description = "SNS topic ARN for alarms"
  value       = module.monitoring.sns_topic_arn
}

output "deployment_info" {
  description = "Information for deployment scripts"
  value = {
    region             = var.aws_region
    environment        = var.environment
    cluster_name       = module.ecs.cluster_name
    ecr_repositories   = module.ecs.ecr_repository_urls
    rds_endpoint       = module.rds.db_endpoint
    alb_dns            = module.ecs.alb_dns_name
  }
  sensitive = true
}
