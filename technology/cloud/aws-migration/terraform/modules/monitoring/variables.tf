variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "ecs_cluster_name" {
  type = string
}

variable "ecs_service_names" {
  type = list(string)
}

variable "rds_instance_id" {
  type = string
}

variable "alb_arn_suffix" {
  type = string
}

variable "enable_cloudwatch_logs" {
  type = bool
}

variable "log_retention_days" {
  type = number
}

variable "alarm_email" {
  type = string
}

variable "tags" {
  type = map(string)
}
