# Makefile for managing LocalStack with Docker Compose and Flask

.PHONY: runlocal down create-bucket-local run-flask create-ec2-local

LOCALSTACK_ECR_ENDPOINT=http://localhost:4566
ECR_REPOSITORY=my-flask-app            # Replace with your LocalStack ECR repository name
IMAGE_TAG=latest

runlocal: down up create-bucket-local build-image run-flask

up:
	docker-compose up -d
	@echo "LocalStack is starting..."

create-bucket-local:
	@echo "Waiting for LocalStack to be ready..."
	@sleep 5  # Adjust sleep time if necessary
	@echo "Creating S3 bucket..."
	@awslocal s3 mb s3://my-file-upload-bucket
	@echo "Bucket created."

.PHONY: create-ec2-local

create-ec2-local:
	@awslocal ec2 run-instances \
		--image-id ami-06b21ccaeff8cd686 \
		--count 1 \
		--instance-type t2.nano --key-name my-key \
		--security-group-ids $$sg_id \



build-image:
	docker build -f Dockerfile.prod -t my-flask-app .

push-image-local:
	# Tag the image for LocalStack ECR
	docker tag my-flask-app:latest localhost:4566/my-flask-app:latest
	# Push the image to LocalStack ECR
	docker push localhost:4566/my-flask-app:latest

run-flask:
	docker run -p 5000:5000 my-flask-app

down:
	docker-compose down

create-ec2:
	aws ec2 run-instances \
		--image-id ami-06b21ccaeff8cd686 \ 
		--count 1 \
		--instance-type t2.micro \ 
		--key-name your-key-pair \  # Replace with your key pair name
		--security-group-ids sg-0123456789abcdef0 \  # Replace with your security group ID

remove-all-containers:
	@docker stop $$(docker ps -q) || true
	@docker rm $$(docker ps -aq) || true

remove-all-images:
	@docker rmi $$(docker images -q) || true
