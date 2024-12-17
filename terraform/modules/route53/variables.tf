variable "route53_zone_id" {
  description = "ID of the Route53 hosted zone"
  type        = string
}

variable "subdomain" {
  description = "Subdomain for the EC2 instance"
  type        = string
}

variable "instance_public_ip" {
  description = "Public IP of the EC2 instance"
  type        = string
}
