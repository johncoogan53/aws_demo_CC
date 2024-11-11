# aws_demo_CC



ssh -i /workspaces/aws_demo_CC/.ssh/aws_demo_pair.pem -o StrictHostKeyChecking=no ec2-user@3.95.201.218

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 673012944196.dkr.ecr.us-east-1.amazonaws.com

docker pull 673012944196.dkr.ecr.us-east-1.amazonaws.com/aws_demo/demo_flask_app:latest

http://127.0.0.1:5000