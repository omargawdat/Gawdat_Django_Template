data "aws_security_group" "existing" {
  id = var.security_group_id
}

resource "aws_launch_template" "main" {
  name_prefix   = "${var.project_name}-launch-template-"
  image_id      = var.ami_id
  instance_type = var.instance_type

  vpc_security_group_ids = [data.aws_security_group.existing.id]

  tags = merge(var.tags, {
    Name = "${var.project_name}-launch-template"
  })
}

resource "aws_instance" "main" {
  launch_template {
    id      = aws_launch_template.main.id
    version = "$Latest"
  }
  tags = merge(var.tags, {
    Name = "${var.project_name}"
  })
}
