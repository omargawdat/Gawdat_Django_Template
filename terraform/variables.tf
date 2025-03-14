variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
}

variable "app_name" {
  description = "The name of the application, used in the service name and subdomain"
  type        = string
}

variable "apprunner_ecr_access_role_arn" {
  description = "ARN of the IAM role that allows App Runner to access ECR"
  type        = string
}

variable "domain_name" {
  description = "The root domain name for the application"
  type        = string
}

variable "ecr_image_identifier" {
  description = "The ECR repository image identifier"
  type        = string
}

variable "container_port" {
  description = "The port the container exposes"
  type        = string
}

variable "media_bucket_name" {
  description = "The name of the S3 bucket for media and static files"
  type        = string
}

variable "secret_manager_name" {
  description = "The name of the AWS Secret Manager secret"
  type        = string
}

variable "db_name" {
  description = "The name of the database"
  type        = string
}
