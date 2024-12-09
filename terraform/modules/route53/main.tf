data "aws_route53_zone" "main" {
  zone_id = var.route53_zone_id
}

resource "aws_route53_record" "subdomain" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = var.subdomain
  type    = "A"
  ttl     = 300
  records = [var.instance_public_ip]
}
