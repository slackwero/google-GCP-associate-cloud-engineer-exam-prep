# Coverage analysis: 2026 blueprint vs. the official learning path

Date: 2026-08-02. A cross-check between the current official exam guide
(2026-06-30, 4 sections) and the 17 activities of the official learning path
(skills.google/paths/11). This analysis is what the reinforcement files of the
question bank come from.

## Do they match?

- The official path **is already aligned with the new exam**: it includes the
  three AI Infrastructure courses (GPU / TPU / deployment types) matching the AI
  topics added in the 2026 guide, and it was updated recently.
- The 5-section Spanish guide is the **previous** version — historical reference
  only.

## Well covered by the path (~70% of the blueprint)

| Blueprint topic | Path activity |
|---|---|
| IAM, projects, hierarchy, APIs (S1) | Essential Infrastructure: Foundation |
| Compute Engine, disks, VPC, Load Balancing (S2/S3) | Essential: Core Services + Elastic + LB badge |
| MIGs, autoscaling, Spot VMs (S2) | Elastic Infrastructure |
| GKE: clusters, kubectl, node pools, HPA/VPA (S2/S3) | Getting Started with GKE + Kubernetes badge |
| Cloud Run / Cloud Run functions, Eventarc, events (S2/S3) | The two Cloud Run courses |
| Database choice: Cloud SQL, AlloyDB, Spanner, Firestore, Bigtable (S2) | Choose a database |
| GPUs vs TPUs, AI deployment (S2/S3) | The three AI Infrastructure courses |
| Monitoring, Logging, Ops Agent, Prometheus (S3.4) | Logging and Monitoring |
| Terraform, IaC (S2.4) | Intro to Terraform + Terraform badge |

## Gaps in the path → reinforcement files in the bank

Sub-topics present in the official guide but missing or only touched on by the
path:

### Section 1 (~20%)
- Billing in depth: budgets, alerts, BigQuery exports
- Organization policies, standalone organizations
- Cloud Identity (user/group management), quotas and quota increases
- **Cloud Asset Inventory + Gemini Cloud Assist for resource analysis**
- **Workforce Identity Federation**

### Section 2 (~30%)
- **Hyperdisk** (vs. zonal/regional PD)
- **Agent Runtime on the Gemini Enterprise Agent Platform**
- **Memorystore, Managed Service for Apache Kafka, Dataflow**
- **Filestore, NetApp Volumes, Managed Lustre**
- Multi-region redundancy in data solutions
- **Cloud NGFW**: policies, secure tags, service accounts in rules
- **Cloud Interconnect**, Network Service Tiers
- **Fabric FAST, Config Connector, Helm**
- **Gemini CLI, Google Antigravity, Application Design Center**

### Section 3 (~30%)
- **Database Center**, **CMEK**
- Storage cost estimation
- Custom static routes
- **Cloud Trace, Cloud Profiler, Query Insights, index advisor**
- **Active Assist**, **Cloud Hub**, **Personalized Service Health**
- **Cloud Workstations**, notebooks (Workbench / BigQuery)
- Audit logs, VPC Flow Logs, firewall logs

### Section 4 (~20%)
- Service account impersonation and short-lived credentials
- **Service accounts with GKE apps + Workload Identity Federation**
- IAM policy inheritance across the organization hierarchy

## How the tool makes up for it

1. `data/blueprint.json` holds the official sub-topics; every question is tagged
   with its sub-topic.
2. **Coverage test**: pytest fails if any sub-topic has fewer than 5 questions →
   100% blueprint coverage is verified, not promised.
3. Dedicated reinforcement questions for the gaps listed above.
4. A dashboard with per-sub-topic coverage and two targets (70% pass mark / 95%
   personal goal).

## "Ready for the exam" criterion

A consistent ≥90% on full mock exams (50 questions, 2 h, weights 20/30/30/20)
through the final stretch.
