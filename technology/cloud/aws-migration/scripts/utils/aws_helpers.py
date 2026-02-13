"""
AWS SDK helper functions
"""
import boto3
from botocore.exceptions import ClientError
from typing import Dict, List, Optional
import json


class AWSHelper:
    """Helper class for AWS operations"""

    def __init__(self, region: str = 'us-east-1'):
        """
        Initialize AWS clients

        Args:
            region: AWS region
        """
        self.region = region
        self.ecs_client = boto3.client('ecs', region_name=region)
        self.ecr_client = boto3.client('ecr', region_name=region)
        self.rds_client = boto3.client('rds', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)
        self.dms_client = boto3.client('dms', region_name=region)
        self.cloudwatch_client = boto3.client('cloudwatch', region_name=region)

    def get_ecr_login_token(self, registry_id: Optional[str] = None) -> Dict:
        """
        Get ECR authentication token

        Args:
            registry_id: ECR registry ID

        Returns:
            Dict with authorization token and endpoint
        """
        try:
            if registry_id:
                response = self.ecr_client.get_authorization_token(registryIds=[registry_id])
            else:
                response = self.ecr_client.get_authorization_token()

            return response['authorizationData'][0]
        except ClientError as e:
            raise Exception(f"Failed to get ECR login token: {e}")

    def list_ecs_services(self, cluster_name: str) -> List[str]:
        """
        List ECS services in a cluster

        Args:
            cluster_name: ECS cluster name

        Returns:
            List of service ARNs
        """
        try:
            response = self.ecs_client.list_services(cluster=cluster_name)
            return response.get('serviceArns', [])
        except ClientError as e:
            raise Exception(f"Failed to list ECS services: {e}")

    def get_rds_endpoint(self, db_identifier: str) -> Dict:
        """
        Get RDS instance endpoint

        Args:
            db_identifier: RDS instance identifier

        Returns:
            Dict with endpoint and port
        """
        try:
            response = self.rds_client.describe_db_instances(
                DBInstanceIdentifier=db_identifier
            )
            db_instance = response['DBInstances'][0]

            return {
                'endpoint': db_instance['Endpoint']['Address'],
                'port': db_instance['Endpoint']['Port'],
                'status': db_instance['DBInstanceStatus']
            }
        except ClientError as e:
            raise Exception(f"Failed to get RDS endpoint: {e}")

    def upload_to_s3(self, bucket: str, key: str, file_path: str) -> bool:
        """
        Upload file to S3

        Args:
            bucket: S3 bucket name
            key: S3 object key
            file_path: Local file path

        Returns:
            True if successful
        """
        try:
            self.s3_client.upload_file(file_path, bucket, key)
            return True
        except ClientError as e:
            raise Exception(f"Failed to upload to S3: {e}")

    def get_cloudwatch_metrics(self, namespace: str, metric_name: str,
                               dimensions: List[Dict], start_time, end_time) -> List:
        """
        Get CloudWatch metrics

        Args:
            namespace: Metric namespace
            metric_name: Metric name
            dimensions: Metric dimensions
            start_time: Start time
            end_time: End time

        Returns:
            List of metric datapoints
        """
        try:
            response = self.cloudwatch_client.get_metric_statistics(
                Namespace=namespace,
                MetricName=metric_name,
                Dimensions=dimensions,
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average', 'Maximum', 'Minimum']
            )
            return response.get('Datapoints', [])
        except ClientError as e:
            raise Exception(f"Failed to get CloudWatch metrics: {e}")
