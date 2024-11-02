# Makefile for managing LocalStack with Docker Compose and Flask

.PHONY: runlocal down create-bucket-local run-flask create-ec2-local

LOCALSTACK_ECR_ENDPOINT=http://localhost:4566
ECR_REPOSITORY=my-flask-app            # Replace with your LocalStack ECR repository name
IMAGE_TAG=latest

runlocal: down up create-bucket-local

up:
	docker-compose up -d
	@echo "LocalStack is starting..."
	@echo "Also starting Flask app..."

create-bucket-local:
	@echo "Waiting for LocalStack to be ready..."
	@sleep 5  # Adjust sleep time if necessary
	@echo "Creating S3 bucket..."
	@awslocal s3 mb s3://my-file-upload-bucket
	@echo "Bucket created."


down:
	docker-compose down

remove-all-containers:
	@docker stop $$(docker ps -q) || true
	@docker rm $$(docker ps -aq) || true

remove-all-images:
	@docker rmi $$(docker images -q) || true
