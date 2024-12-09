variable "region" {
  description = "AWS region"
  type        = string
}

variable "security_group_id" {
  description = "ID of the security group"
  type        = string
}

variable "ami_id" {
  description = "ID of the AMI to use for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "Instance type for the EC2 instance"
  type        = string
}

variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "route53_zone_id" {
  description = "ID of the Route53 hosted zone"
  type        = string
}

variable "subdomain" {
  description = "Subdomain for the EC2 instance"
  type        = string
}

variable "tags" {
  description = "Tags to apply to resources"
  type = map(string)
}

variable "github_repo_url" {
  description = "URL of the GitHub repository"
  type        = string
}

variable "repo_folder_name" {
  description = "Name of the folder to clone the repository into"
  type        = string
}

variable "ssh_key_path" {
  description = "Path to the SSH private key"
  type        = string
}
