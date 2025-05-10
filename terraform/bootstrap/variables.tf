variable "region" {
  description = "AWS region for state resources"
  type        = string
  default = "eu-central-1"
}

variable "state_bucket_name" {
  description = "Name of the S3 bucket for Terraform state"
  type        = string
  default = "gawdat-company-terraform-states"
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table for Terraform state locks"
  type        = string
  default = "gawdat-company-terraform-locks"
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  type        = string
  default     = "gawdat-company-ecr"
}
