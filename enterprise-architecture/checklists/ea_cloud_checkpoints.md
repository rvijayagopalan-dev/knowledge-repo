

## New structure of the checklist (what you’ll see)

Your table now has these columns:

| Gate | Checkpoint | Required Evidence | **AWS Controls** | **Azure Controls** | **GCP Controls** | Status | Notes |

---

## Examples of cloud alignment (by gate)

### **Gate 0 – Intake**

| Checkpoint          | AWS                               | Azure              | GCP                      |
| ------------------- | --------------------------------- | ------------------ | ------------------------ |
| Strategic alignment | Well-Architected – Business Value | CAF Strategy       | GCP WAF – Business Value |
| High-level risks    | Security Hub                      | Defender for Cloud | Security Command Center  |

### **Gate 1 – Concept**

| Checkpoint            | AWS           | Azure                 | GCP                   |
| --------------------- | ------------- | --------------------- | --------------------- |
| Initial business case | Cost Explorer | Azure Cost Management | Cloud Billing         |
| FinOps estimate       | AWS Budgets   | Azure Budgets         | Cloud Billing Budgets |

### **Gate 2 – Architecture Direction**

| Checkpoint             | AWS                   | Azure                       | GCP                      |
| ---------------------- | --------------------- | --------------------------- | ------------------------ |
| Landing zone alignment | **AWS Control Tower** | **Azure CAF Landing Zones** | **GCP Cloud Foundation** |
| Data architecture      | S3 + Glue Catalog     | ADLS Gen2 + Purview         | GCS + Data Catalog       |
| Integration approach   | API Gateway / MSK     | APIM / Event Hubs           | Apigee / Pub/Sub         |

### **Gate 3 – Detailed Design**

| Checkpoint    | AWS                   | Azure                           | GCP                   |
| ------------- | --------------------- | ------------------------------- | --------------------- |
| Threat model  | IAM + KMS + GuardDuty | Entra ID + Key Vault + Defender | IAM + Cloud KMS + SCC |
| Observability | CloudWatch            | Azure Monitor                   | Cloud Operations      |

### **Gate 4 – Pre-Test**

| Checkpoint | AWS                      | Azure           | GCP              |
| ---------- | ------------------------ | --------------- | ---------------- |
| IaC        | CloudFormation/Terraform | Bicep/Terraform | Terraform        |
| CI/CD      | CodePipeline/GitHub      | Azure DevOps    | Cloud Build      |
| Monitoring | CloudWatch Dashboards    | Azure Monitor   | Cloud Monitoring |

### **Gate 5 – Go-Live**

| Checkpoint       | AWS              | Azure                     | GCP                     |
| ---------------- | ---------------- | ------------------------- | ----------------------- |
| Security testing | AWS Inspector    | Defender for Cloud        | Security Command Center |
| Runbooks         | SSM + AWS Backup | Azure Automation + Backup | Cloud Runbooks + Backup |

### **Gate 6 – Operate**

| Checkpoint      | AWS             | Azure              | GCP                   |
| --------------- | --------------- | ------------------ | --------------------- |
| Stability       | CloudWatch SLOs | Azure Monitor SLOs | Cloud Monitoring SLOs |
| Cost            | Cost Explorer   | Azure Cost Mgmt    | Cloud Billing         |
| Lessons learned | ADR Repo (Git)  | ADR Repo (Git)     | ADR Repo (Git)        |

---