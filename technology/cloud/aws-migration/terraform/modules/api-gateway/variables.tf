variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "alb_listener_arn" {
  type = string
}

variable "alb_dns_name" {
  type = string
}

variable "stage_name" {
  type = string
}

variable "tags" {
  type = map(string)
}
