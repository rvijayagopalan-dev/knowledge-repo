# AWS Migration Runbook

Complete step-by-step guide for migrating on-premise microservices to AWS.

## Table of Contents
1. [Pre-Migration Checklist](#pre-migration-checklist)
2. [Phase 1: Assessment](#phase-1-assessment)
3. [Phase 2: Infrastructure Setup](#phase-2-infrastructure-setup)
4. [Phase 3: Application Migration](#phase-3-application-migration)
5. [Phase 4: Data Migration](#phase-4-data-migration)
6. [Phase 5: Cutover](#phase-5-cutover)
7. [Phase 6: Post-Migration](#phase-6-post-migration)
8. [Rollback Procedures](#rollback-procedures)

---

## Pre-Migration Checklist

### Prerequisites
- [ ] AWS account with administrator access
- [ ] AWS CLI installed and configured
- [ ] Terraform >= 1.5.0 installed
- [ ] Docker installed
- [ ] Python 3.9+ installed
- [ ] Access to on-premise infrastructure
- [ ] VPN/Direct Connect configured (if needed)

### Documentation Prepared
- [ ] Current architecture diagram
- [ ] Service dependency map
- [ ] Database schemas
- [ ] API documentation
- [ ] Environment variables list
- [ ] DNS records list

### Stakeholder Approval
- [ ] Migration plan approved by management
- [ ] Budget approved
- [ ] Maintenance window scheduled
- [ ] Communication plan in place

---

## Phase 1: Assessment

### 1.1 Run Pre-Migration Assessment

```bash
cd technology/cloud/aws-migration

python scripts/migration/pre_migration_assessment.py \
  --config config/migration-config.yaml \
  --output assessment-report.json
```

### 1.2 Review Assessment Report

Open `assessment-report.json` and review:
- Resource inventory (services, databases, storage)
- AWS service recommendations
- Estimated monthly costs
- Migration recommendations

### 1.3 Customize Configuration

Edit `config/migration-config.yaml`:
```yaml
migration:
  source:
    databases:
      - name: <your-db-name>
        type: postgresql
        host: <your-db-host>
        port: 5432
        size_gb: <database-size>

  target:
    region: us-east-1
    services:
      - name: <service-name>
        cpu: 512
        memory: 1024
```

### 1.4 Cost Approval

- Review estimated costs from assessment
- Get budget approval from finance team
- Document cost allocation tags

**Deliverables:**
- ✅ Assessment report
- ✅ Migration configuration files
- ✅ Budget approval

---

## Phase 2: Infrastructure Setup

### 2.1 Configure Terraform Variables

Edit `terraform/environments/prod.tfvars`:
```hcl
aws_region   = "us-east-1"
environment  = "production"
project_name = "your-project"

# Customize VPC, ECS, RDS settings
```

### 2.2 Initialize Terraform

```bash
cd terraform

terraform init

# Verify initialization
terraform version
```

### 2.3 Review Infrastructure Plan

```bash
terraform plan -var-file=environments/prod.tfvars -out=plan.out

# Review the plan carefully
# Expected resources: VPC, Subnets, ECS, RDS, ALB, CloudWatch
```

**Critical Review Points:**
- ✅ VPC CIDR doesn't conflict with on-premise
- ✅ Availability zones are correct
- ✅ RDS Multi-AZ is enabled for production
- ✅ Security groups have appropriate rules

### 2.4 Apply Infrastructure

```bash
# Apply the plan
terraform apply plan.out

# Wait for completion (15-30 minutes)
```

### 2.5 Verify Infrastructure

```bash
# Save outputs
terraform output -json > ../terraform-outputs.json

# Verify VPC
aws ec2 describe-vpcs --filters "Name=tag:Project,Values=your-project"

# Verify ECS cluster
aws ecs describe-clusters --clusters <cluster-name>

# Verify RDS
aws rds describe-db-instances --db-instance-identifier <db-identifier>
```

**Deliverables:**
- ✅ AWS infrastructure provisioned
- ✅ Terraform state saved
- ✅ Infrastructure verified

---

## Phase 3: Application Migration

### 3.1 Containerize Applications

For each microservice:

```bash
cd docker/<service-name>

# Copy your application code
cp -r /path/to/on-premise/app ./app/

# Test locally
docker build -t <service-name>:test .
docker run -p 8080:8080 <service-name>:test

# Verify health endpoint
curl http://localhost:8080/health
```

### 3.2 Test with Docker Compose

```bash
cd docker/microservice-template

# Update docker-compose.yml with your services
docker-compose up

# Test inter-service communication
curl http://localhost:8080/api/info
```

### 3.3 Build and Push to ECR

Get AWS account ID:
```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=us-east-1
```

Login to ECR:
```bash
aws ecr get-login-password --region $REGION | \
  docker login --username AWS --password-stdin \
  $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
```

Build and push:
```bash
python scripts/deployment/build_and_push_images.py \
  --services user-service,order-service \
  --version v1.0.0 \
  --region $REGION
```

### 3.4 Deploy to ECS

The services are automatically created by Terraform. Update task definitions:

```bash
# Get current task definition
aws ecs describe-task-definition \
  --task-definition <task-family> > task-def.json

# Register new version (update image tag in task-def.json)
aws ecs register-task-definition --cli-input-json file://task-def.json

# Update service to use new task definition
aws ecs update-service \
  --cluster <cluster-name> \
  --service <service-name> \
  --task-definition <task-family>:v1.0.0
```

### 3.5 Verify Deployment

```bash
# Check service status
aws ecs describe-services \
  --cluster <cluster-name> \
  --services <service-name>

# Check running tasks
aws ecs list-tasks \
  --cluster <cluster-name> \
  --service-name <service-name>

# View logs
aws logs tail /ecs/<service-name> --follow
```

**Deliverables:**
- ✅ All services containerized
- ✅ Images pushed to ECR
- ✅ Services deployed to ECS
- ✅ Health checks passing

---

## Phase 4: Data Migration

### 4.1 Database Migration Planning

**Options:**
1. **AWS DMS** (Recommended for minimal downtime)
2. **pg_dump/pg_restore** (for PostgreSQL)
3. **mysqldump** (for MySQL)

### 4.2 Using AWS DMS

Create DMS replication instance:
```bash
aws dms create-replication-instance \
  --replication-instance-identifier migration-instance \
  --replication-instance-class dms.t3.medium \
  --allocated-storage 100
```

Create source endpoint:
```bash
aws dms create-endpoint \
  --endpoint-identifier source-db \
  --endpoint-type source \
  --engine-name postgres \
  --username <db-user> \
  --password <db-password> \
  --server-name <on-prem-host> \
  --port 5432 \
  --database-name <db-name>
```

Create target endpoint:
```bash
aws dms create-endpoint \
  --endpoint-identifier target-db \
  --endpoint-type target \
  --engine-name postgres \
  --username <rds-user> \
  --password <rds-password> \
  --server-name <rds-endpoint> \
  --port 5432 \
  --database-name <db-name>
```

Create migration task:
```bash
aws dms create-replication-task \
  --replication-task-identifier migration-task \
  --source-endpoint-arn <source-endpoint-arn> \
  --target-endpoint-arn <target-endpoint-arn> \
  --replication-instance-arn <replication-instance-arn> \
  --migration-type full-load-and-cdc \
  --table-mappings file://table-mappings.json
```

Monitor migration:
```bash
aws dms describe-replication-tasks \
  --filters "Name=replication-task-identifier,Values=migration-task"
```

### 4.3 File Storage Migration

Sync files to S3:
```bash
# Install AWS CLI
pip install awscli

# Sync files
aws s3 sync /on-premise/data/ s3://<bucket-name>/data/ \
  --storage-class STANDARD_IA \
  --delete
```

### 4.4 Validate Data

```bash
# Connect to RDS
psql -h <rds-endpoint> -U <db-user> -d <db-name>

# Check row counts
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM orders;

# Verify data integrity
SELECT * FROM users ORDER BY created_at DESC LIMIT 10;
```

**Deliverables:**
- ✅ Database migrated to RDS
- ✅ Data integrity verified
- ✅ Files migrated to S3
- ✅ Replication lag < 1 second (for DMS)

---

## Phase 5: Cutover

### 5.1 Pre-Cutover Checklist

- [ ] All services deployed and healthy
- [ ] Database replication complete
- [ ] Data validation passed
- [ ] Load testing completed
- [ ] Rollback plan ready
- [ ] Team on standby

### 5.2 Traffic Cutover Strategy

**Option A: DNS Cutover (Recommended)**
1. Lower DNS TTL to 60 seconds (24 hours before cutover)
2. Update DNS to point to AWS ALB
3. Monitor traffic shift
4. Keep on-premise systems running for rollback

**Option B: Blue-Green Deployment**
1. Keep on-premise as "blue" environment
2. AWS as "green" environment
3. Gradually route traffic using weighted routing

### 5.3 Execute Cutover

```bash
# Get ALB DNS name
ALB_DNS=$(terraform output -raw alb_dns_name)

# Update DNS (example with Route 53)
aws route53 change-resource-record-sets \
  --hosted-zone-id <zone-id> \
  --change-batch file://dns-change.json
```

Example `dns-change.json`:
```json
{
  "Changes": [{
    "Action": "UPSERT",
    "ResourceRecordSet": {
      "Name": "app.example.com",
      "Type": "CNAME",
      "TTL": 60,
      "ResourceRecords": [{"Value": "<alb-dns>"}]
    }
  }]
}
```

### 5.4 Monitor Cutover

```bash
# Watch CloudWatch metrics
aws cloudwatch get-dashboard --dashboard-name <dashboard-name>

# Monitor ECS services
watch -n 10 'aws ecs describe-services \
  --cluster <cluster> --services <service> \
  --query "services[0].{Desired:desiredCount,Running:runningCount}"'

# Check ALB health checks
aws elbv2 describe-target-health \
  --target-group-arn <target-group-arn>

# Monitor logs
aws logs tail /ecs/<service-name> --follow
```

**Deliverables:**
- ✅ Traffic successfully routed to AWS
- ✅ No errors in logs
- ✅ CloudWatch metrics within normal range
- ✅ All health checks passing

---

## Phase 6: Post-Migration

### 6.1 Validation Testing

Run comprehensive tests:
```bash
python scripts/migration/post_migration_validation.py \
  --config config/services-config.yaml \
  --report validation-report.json
```

### 6.2 Performance Testing

```bash
# Install Apache Bench
apt-get install apache2-utils

# Load test
ab -n 10000 -c 100 http://<alb-dns>/api/health

# Monitor performance
watch -n 5 'aws cloudwatch get-metric-statistics \
  --namespace AWS/ApplicationELB \
  --metric-name TargetResponseTime \
  --start-time $(date -u -d "5 minutes ago" +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average'
```

### 6.3 Cost Monitoring

```bash
# Check actual costs
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "7 days ago" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity DAILY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE
```

### 6.4 Decommission On-Premise

**Wait 2-4 weeks before decommissioning!**

- [ ] Monitor AWS environment for stability
- [ ] Verify all functionality working
- [ ] Backup on-premise data
- [ ] Document lessons learned
- [ ] Decommission on-premise infrastructure

**Deliverables:**
- ✅ All tests passing
- ✅ Performance meets SLAs
- ✅ Costs within budget
- ✅ On-premise decommissioned (after stabilization)

---

## Rollback Procedures

### Immediate Rollback (DNS)

```bash
# Revert DNS to on-premise
aws route53 change-resource-record-sets \
  --hosted-zone-id <zone-id> \
  --change-batch file://dns-rollback.json

# Verify rollback
dig app.example.com

# Monitor on-premise systems
```

### ECS Service Rollback

```bash
# Rollback to previous task definition
aws ecs update-service \
  --cluster <cluster> \
  --service <service> \
  --task-definition <previous-task-def>

# Verify rollback
aws ecs describe-services \
  --cluster <cluster> \
  --services <service>
```

### Database Rollback (DMS)

If using DMS with CDC (Change Data Capture):
```bash
# Reverse replication direction
# Create reverse DMS task from RDS to on-premise
# This requires planning before migration!
```

---

## Emergency Contacts

- **AWS Support**: [Support Case Portal]
- **Team Lead**: [Contact Info]
- **Database Admin**: [Contact Info]
- **DevOps Lead**: [Contact Info]

---

## Post-Migration Optimization

### Week 1-2
- Monitor all CloudWatch alarms
- Analyze application logs
- Fine-tune auto-scaling policies
- Review security group rules

### Week 3-4
- Cost optimization review
- Right-size ECS tasks
- Evaluate RDS reserved instances
- Implement S3 lifecycle policies

### Month 2-3
- Set up CI/CD pipeline
- Implement disaster recovery
- Add advanced monitoring (APM)
- Security audit

---

## Success Criteria

- ✅ All services running on AWS
- ✅ Zero data loss
- ✅ Downtime < planned maintenance window
- ✅ Performance meets or exceeds on-premise
- ✅ Costs within budget
- ✅ No critical issues for 2 weeks

---

**Migration Complete!** 🎉

For ongoing support, refer to the main [README.md](../README.md) and AWS documentation.
