An **audit-ready ARB checklist aligned to ISO 27001 and SOC 2** 

## What makes this “audit-ready”

Your checklist now uses a control-centric format typically accepted by ISO 27001 and SOC 2 auditors, with these additional columns:

| New Column                     | Why it matters for audit                                                                     |
| ------------------------------ | -------------------------------------------------------------------------------------------- |
| **Control Domain**             | Maps each checkpoint to a control area (e.g., Governance, Risk, Access Control, Monitoring). |
| **Control ID (ISO/SOC2)**      | Explicit linkage to relevant clauses (e.g., ISO 27001 A.9, A.12; SOC2 CC1–CC9).              |
| **AWS / Azure / GCP Controls** | Shows the concrete cloud services that implement the control.                                |
| **Evidence Owner**             | Clear accountability for producing audit evidence.                                           |
| **Retention (years)**          | How long evidence must be kept (audit trail).                                                |
| **Mandatory?**                 | Flags what must exist vs. what is optional.                                                  |

---

## Examples of how checkpoints are mapped

### **Gate 2 – Landing Zone Alignment**

* **Control Domain:** Access Control
* **Control ID:** ISO 27001 A.9 / SOC2 CC6
* **AWS:** Control Tower
* **Azure:** CAF Landing Zones
* **GCP:** Cloud Foundation
* **Evidence Owner:** Platform Lead
* **Retention:** 5 years
* **Mandatory:** Yes

### **Gate 3 – Security Threat Model**

* **Control Domain:** Risk Treatment
* **Control ID:** ISO 27001 A.6.1 / SOC2 CC4
* **AWS:** IAM + KMS + GuardDuty
* **Azure:** Entra ID + Key Vault + Defender
* **GCP:** IAM + Cloud KMS + Security Command Center

### **Gate 5 – Runbooks Created**

* **Control Domain:** Incident Management
* **Control ID:** ISO 27001 A.16 / SOC2 CC7
* **AWS:** SSM + AWS Backup
* **Azure:** Automation + Backup
* **GCP:** Cloud Runbooks + Backup

### **Gate 6 – System Stability**

* **Control Domain:** Operations
* **Control ID:** ISO 27001 A.12.4 / SOC2 CC7
* **AWS:** CloudWatch SLOs
* **Azure:** Azure Monitor SLOs
* **GCP:** Cloud Monitoring SLOs

---
