terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.90.0"
    }
  }
  backend "s3" {}
}

provider "aws" {
  region = var.aws_region
}

data "aws_route53_zone" "existing" {
  name = var.parent_domain
}

resource "aws_apprunner_service" "example" {
  service_name = replace(var.domain_name, ".", "-")

  source_configuration {
    authentication_configuration {
      access_role_arn = var.apprunner_ecr_access_role_arn
    }

    auto_deployments_enabled = false

    image_repository {
      image_configuration {
        port = var.container_port
        runtime_environment_variables = {
          "AWS_REGION_NAME"         = var.aws_region
          "AWS_SECRET_MANAGER_NAME" = var.secret_manager_name
          "IS_LOCAL"                = "false"
          "DOMAIN_NAME"             = var.domain_name
          "S3_BUCKET_NAME"          = var.media_bucket_name
          "DB_NAME"                 = var.db_name
        }
      }
      image_identifier = var.ecr_image_identifier
      image_repository_type = "ECR"
    }
  }

  instance_configuration {
    instance_role_arn = var.apprunner_instance_role_arn
  }
}

resource "aws_apprunner_custom_domain_association" "example" {
  domain_name = var.domain_name
  service_arn = aws_apprunner_service.example.arn
  enable_www_subdomain = false
}

resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_apprunner_custom_domain_association.example.certificate_validation_records : dvo.name => dvo
  }

  zone_id = data.aws_route53_zone.existing.zone_id
  name    = each.value.name
  type    = each.value.type
  records = [each.value.value]
  ttl     = 60
}

# Create CNAME record to point the domain to the App Runner service
resource "aws_route53_record" "cname" {
  zone_id = data.aws_route53_zone.existing.zone_id
  name    = var.domain_name
  type    = "CNAME"
  records = [aws_apprunner_custom_domain_association.example.dns_target]
  ttl     = 300
}

# Create S3 bucket for media and static files
resource "aws_s3_bucket" "media_bucket" {
  bucket = var.media_bucket_name
}

# Allow public access to the bucket's objects
resource "aws_s3_bucket_public_access_block" "media_bucket" {
  bucket = aws_s3_bucket.media_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# Set bucket policy to allow public read access
resource "aws_s3_bucket_policy" "media_bucket" {
  bucket = aws_s3_bucket.media_bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.media_bucket.arn}/*"
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.media_bucket]
}

# CORS configuration for the media bucket
resource "aws_s3_bucket_cors_configuration" "media_bucket" {
  bucket = aws_s3_bucket.media_bucket.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
    expose_headers = []
    max_age_seconds = 3000
  }
}
