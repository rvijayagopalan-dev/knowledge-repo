#!/usr/bin/env python3
"""
Pre-migration assessment script
Analyzes on-premise infrastructure and generates migration assessment report
"""
import argparse
import json
import sys
import os
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.logger import setup_logger
from utils.config import Config


class PreMigrationAssessment:
    """Pre-migration assessment and planning"""

    def __init__(self, config_file: str):
        self.logger = setup_logger('PreMigrationAssessment')
        self.config = Config(config_file)
        self.assessment_report = {
            'timestamp': datetime.now().isoformat(),
            'source_environment': {},
            'target_environment': {},
            'resource_inventory': {},
            'migration_recommendations': [],
            'estimated_cost': {}
        }

    def analyze_databases(self):
        """Analyze on-premise databases"""
        self.logger.info("Analyzing databases...")

        databases = self.config.get('migration.source.databases', [])
        db_inventory = []

        for db in databases:
            db_info = {
                'name': db.get('name'),
                'type': db.get('type'),
                'host': db.get('host'),
                'port': db.get('port'),
                'estimated_size_gb': db.get('size_gb', 'unknown'),
                'aws_target': self._recommend_rds_instance(db.get('type'))
            }
            db_inventory.append(db_info)
            self.logger.info(f"  - {db_info['name']}: {db_info['type']}")

        self.assessment_report['resource_inventory']['databases'] = db_inventory
        return db_inventory

    def analyze_storage(self):
        """Analyze on-premise storage"""
        self.logger.info("Analyzing storage...")

        storage = self.config.get('migration.source.storage', [])
        storage_inventory = []

        for stor in storage:
            storage_info = {
                'path': stor.get('path'),
                'size_gb': stor.get('size_gb'),
                'aws_target': 'S3',
                'estimated_migration_time_hours': stor.get('size_gb', 0) / 10  # Rough estimate
            }
            storage_inventory.append(storage_info)
            self.logger.info(f"  - {storage_info['path']}: {storage_info['size_gb']} GB")

        self.assessment_report['resource_inventory']['storage'] = storage_inventory
        return storage_inventory

    def analyze_services(self):
        """Analyze microservices"""
        self.logger.info("Analyzing services...")

        services = self.config.get('migration.target.services', [])
        service_inventory = []

        for svc in services:
            service_info = {
                'name': svc.get('name'),
                'type': svc.get('type'),
                'cpu': svc.get('cpu'),
                'memory': svc.get('memory'),
                'aws_target': 'ECS Fargate'
            }
            service_inventory.append(service_info)
            self.logger.info(f"  - {service_info['name']}: {service_info['cpu']} CPU, {service_info['memory']} Memory")

        self.assessment_report['resource_inventory']['services'] = service_inventory
        return service_inventory

    def estimate_costs(self):
        """Estimate AWS costs"""
        self.logger.info("Estimating AWS costs...")

        # Rough cost estimates (monthly)
        costs = {
            'ecs_fargate': 0,
            'rds': 0,
            's3': 0,
            'data_transfer': 0,
            'total_monthly': 0
        }

        # ECS Fargate costs (rough estimate)
        services = self.assessment_report['resource_inventory'].get('services', [])
        for svc in services:
            cpu = svc.get('cpu', 0)
            memory = svc.get('memory', 0)
            # Fargate pricing: ~$0.04048/vCPU/hour + $0.004445/GB/hour
            hourly_cost = (cpu / 1024 * 0.04048) + (memory / 1024 * 0.004445)
            monthly_cost = hourly_cost * 730  # hours per month
            costs['ecs_fargate'] += monthly_cost

        # RDS costs (rough estimate)
        databases = self.assessment_report['resource_inventory'].get('databases', [])
        costs['rds'] = len(databases) * 200  # Rough $200/month per instance

        # S3 costs
        storage = self.assessment_report['resource_inventory'].get('storage', [])
        total_storage_gb = sum([s.get('size_gb', 0) for s in storage])
        costs['s3'] = total_storage_gb * 0.023  # $0.023/GB/month

        costs['total_monthly'] = sum([
            costs['ecs_fargate'],
            costs['rds'],
            costs['s3']
        ])

        self.assessment_report['estimated_cost'] = costs
        return costs

    def generate_recommendations(self):
        """Generate migration recommendations"""
        self.logger.info("Generating recommendations...")

        recommendations = [
            "Use AWS DMS for database migration with minimal downtime",
            "Containerize applications using Docker for ECS deployment",
            "Implement blue-green deployment for zero-downtime cutover",
            "Enable CloudWatch monitoring for all services",
            "Use AWS Secrets Manager for database credentials",
            "Set up Multi-AZ RDS for high availability",
            "Configure auto-scaling for ECS services based on metrics"
        ]

        self.assessment_report['migration_recommendations'] = recommendations
        return recommendations

    def run_assessment(self) -> dict:
        """Run complete assessment"""
        self.logger.info("Starting pre-migration assessment...")

        self.analyze_databases()
        self.analyze_storage()
        self.analyze_services()
        self.estimate_costs()
        self.generate_recommendations()

        self.logger.info("Assessment complete!")
        return self.assessment_report

    def save_report(self, output_file: str):
        """Save assessment report to file"""
        with open(output_file, 'w') as f:
            json.dump(self.assessment_report, f, indent=2)

        self.logger.info(f"Report saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Pre-migration assessment')
    parser.add_argument('--config', required=True, help='Migration configuration file')
    parser.add_argument('--output', default='assessment-report.json', help='Output report file')

    args = parser.parse_args()

    assessment = PreMigrationAssessment(args.config)
    report = assessment.run_assessment()
    assessment.save_report(args.output)

    print(f"\n{'='*60}")
    print("ASSESSMENT SUMMARY")
    print(f"{'='*60}")
    print(f"Databases: {len(report['resource_inventory'].get('databases', []))}")
    print(f"Services: {len(report['resource_inventory'].get('services', []))}")
    print(f"Storage: {sum([s.get('size_gb', 0) for s in report['resource_inventory'].get('storage', [])])} GB")
    print(f"\nEstimated Monthly Cost: ${report['estimated_cost']['total_monthly']:.2f}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
