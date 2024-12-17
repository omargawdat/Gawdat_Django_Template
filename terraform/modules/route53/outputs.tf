output "fqdn" {
  description = "Fully Qualified Domain Name for the created Route53 record"
  value       = aws_route53_record.subdomain.fqdn
}

output "name" {
  description = "The name of the Route53 record"
  value       = aws_route53_record.subdomain.name
}

output "record_type" {
  description = "The record type of the Route53 record"
  value       = aws_route53_record.subdomain.type
}
