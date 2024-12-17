output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.main.public_ip
}

output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.main.id
}

output "launch_template_id" {
  description = "ID of the created launch template"
  value       = aws_launch_template.main.id
}
