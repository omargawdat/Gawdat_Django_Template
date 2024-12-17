provider "aws" {
  region = var.region
}

locals {
  environment  = terraform.workspace
  project_name = "${var.project_name}-${local.environment}"
  subdomain    = "${local.environment}.${var.subdomain}"
}

module "ec2" {
  source = "./modules/ec2"

  security_group_id = var.security_group_id
  ami_id            = var.ami_id
  instance_type     = var.instance_type
  project_name      = local.project_name
  tags = merge(var.tags, { Environment = local.environment })
}

resource "null_resource" "setup_server" {
  triggers = {
    instance_id = module.ec2.instance_id
  }
  provisioner "local-exec" {
    command = "${path.root}/../scripts/setup_server.sh"
    environment = {
      EC2_PUBLIC_IP       = module.ec2.instance_public_ip
      TERRAFORM_WORKSPACE = local.environment
      GITHUB_REPO_URL     = var.github_repo_url
      REPO_FOLDER_NAME    = var.repo_folder_name
      SSH_KEY_PATH        = var.ssh_key_path
    }
  }
}

module "s3" {
  source = "./modules/s3"

  project_name = local.project_name
  tags = merge(var.tags, { Environment = local.environment })
}

module "route53" {
  source = "./modules/route53"

  route53_zone_id    = var.route53_zone_id
  subdomain          = local.subdomain
  instance_public_ip = module.ec2.instance_public_ip
}
