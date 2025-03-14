output "region" {
  value       = var.region
  description = "AWS region used for resources"
}

output "state_bucket_name" {
  value       = aws_s3_bucket.terraform_state.bucket
  description = "Name of the S3 bucket for Terraform state"
}

output "dynamodb_table_name" {
  value       = aws_dynamodb_table.terraform_locks.name
  description = "Name of the DynamoDB table for state locking"
}

output "apprunner_ecr_access_role_arn" {
  value       = aws_iam_role.apprunner_ecr_access_role.arn
  description = "ARN of the IAM role for App Runner to access ECR"
}
