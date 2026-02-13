output "cluster_id" {
  value = aws_ecs_cluster.main.id
}

output "cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "alb_dns_name" {
  value = aws_lb.main.dns_name
}

output "alb_zone_id" {
  value = aws_lb.main.zone_id
}

output "alb_arn" {
  value = aws_lb.main.arn
}

output "alb_arn_suffix" {
  value = aws_lb.main.arn_suffix
}

output "alb_listener_arn" {
  value = aws_lb_listener.http.arn
}

output "ecr_repository_urls" {
  value = { for k, v in aws_ecr_repository.services : k => v.repository_url }
}

output "ecs_task_security_group_id" {
  value = var.ecs_tasks_security_group_id
}
