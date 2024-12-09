output "environment" {
  description = "Current environment (workspace)"
  value       = terraform.workspace
}

output "ec2_instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = module.ec2.instance_public_ip
}

output "s3_bucket_name" {
  description = "Name of the created S3 bucket"
  value       = module.s3.bucket_name
}

output "route53_fqdn" {
  description = "Fully Qualified Domain Name for the created Route53 record"
  value       = module.route53.fqdn
}

output "project_name" {
  description = "Project name with environment"
  value       = local.project_name
}

output "github_repo_url" {
  value = var.github_repo_url
}

output "repo_folder_name" {
  value = var.repo_folder_name
}

output "ssh_key_path" {
  value = var.ssh_key_path
}
