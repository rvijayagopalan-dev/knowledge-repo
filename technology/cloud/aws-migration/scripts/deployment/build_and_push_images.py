#!/usr/bin/env python3
"""
Build Docker images and push to Amazon ECR
"""
import argparse
import subprocess
import base64
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.logger import setup_logger
from utils.aws_helpers import AWSHelper


class DockerImageBuilder:
    """Build and push Docker images to ECR"""

    def __init__(self, region: str):
        self.logger = setup_logger('DockerImageBuilder')
        self.aws_helper = AWSHelper(region)
        self.region = region

    def ecr_login(self) -> bool:
        """Authenticate Docker with ECR"""
        self.logger.info("Authenticating with ECR...")

        try:
            token_data = self.aws_helper.get_ecr_login_token()
            auth_token = base64.b64decode(token_data['authorizationToken']).decode('utf-8')
            username, password = auth_token.split(':')
            registry = token_data['proxyEndpoint']

            # Docker login
            login_cmd = f'docker login -u {username} -p {password} {registry}'
            result = subprocess.run(login_cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                self.logger.info("ECR authentication successful")
                return True
            else:
                self.logger.error(f"ECR authentication failed: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to authenticate with ECR: {e}")
            return False

    def build_image(self, service_name: str, dockerfile_path: str, tag: str) -> bool:
        """
        Build Docker image

        Args:
            service_name: Service name
            dockerfile_path: Path to Dockerfile directory
            tag: Image tag

        Returns:
            True if successful
        """
        self.logger.info(f"Building image for {service_name}...")

        try:
            build_cmd = f'docker build -t {service_name}:{tag} {dockerfile_path}'
            result = subprocess.run(build_cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                self.logger.info(f"Image built successfully: {service_name}:{tag}")
                return True
            else:
                self.logger.error(f"Image build failed: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to build image: {e}")
            return False

    def push_image(self, service_name: str, ecr_repository_url: str, tag: str) -> bool:
        """
        Push Docker image to ECR

        Args:
            service_name: Service name
            ecr_repository_url: ECR repository URL
            tag: Image tag

        Returns:
            True if successful
        """
        self.logger.info(f"Pushing image to ECR: {ecr_repository_url}...")

        try:
            # Tag image for ECR
            tag_cmd = f'docker tag {service_name}:{tag} {ecr_repository_url}:{tag}'
            subprocess.run(tag_cmd, shell=True, check=True)

            # Push to ECR
            push_cmd = f'docker push {ecr_repository_url}:{tag}'
            result = subprocess.run(push_cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                self.logger.info(f"Image pushed successfully: {ecr_repository_url}:{tag}")
                return True
            else:
                self.logger.error(f"Image push failed: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to push image: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='Build and push Docker images to ECR')
    parser.add_argument('--services', required=True, help='Comma-separated list of services')
    parser.add_argument('--version', default='latest', help='Image version tag')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    parser.add_argument('--ecr-prefix', default='microservices-migration-production',
                       help='ECR repository prefix')

    args = parser.parse_args()

    builder = DockerImageBuilder(args.region)

    # ECR login
    if not builder.ecr_login():
        sys.exit(1)

    # Build and push each service
    services = [s.strip() for s in args.services.split(',')]
    account_id = boto3.client('sts').get_caller_identity()['Account']

    for service in services:
        ecr_url = f"{account_id}.dkr.ecr.{args.region}.amazonaws.com/{args.ecr_prefix}-{service}"

        # Build image
        if not builder.build_image(service, f'./docker/{service}', args.version):
            continue

        # Push image
        builder.push_image(service, ecr_url, args.version)

    print("\n✓ Build and push complete!")


if __name__ == '__main__':
    import boto3
    main()
