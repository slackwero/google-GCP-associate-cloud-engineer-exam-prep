# Official resources — Google Associate Cloud Engineer (ACE)

Reviewed on 2026-08-02.

> ⚠️ **Important:** the exam was refreshed with a **new guide effective
> 2026-06-30** (a 4-section blueprint). The 5-section Spanish guide is the
> PREVIOUS version. Study against the new one.

## Links

| Resource | URL |
|---|---|
| **CURRENT exam guide (effective 2026-06-30, English)** | https://services.google.com/fh/files/misc/063026_associate_cloud_engineer_exam_guide_english.pdf |
| Previous exam guide (Spanish, 5 sections) | https://services.google.com/fh/files/misc/associate_cloud_engineer_exam_guide_spanish.pdf |
| Certification page | https://cloud.google.com/learn/certification/cloud-engineer |
| **Official learning path (study priority)** | https://www.skills.google/paths/11 |
| Official sample questions | https://docs.google.com/forms/d/e/1FAIpQLSewdU5twM8Y9zY4Z7Syo1M7oikGuKACB_UN5XBRJDlnpAV9Bw/viewform |
| Exam registration | https://cp.certmetrics.com/google/en/login |

Local copies: [`guia-examen-ace-2026-06-30-en.pdf`](guia-examen-ace-2026-06-30-en.pdf)
(current) · [`guia-examen-ace-es.pdf`](guia-examen-ace-es.pdf) (previous)

## Exam facts

- **Length:** 2 hours — **50-60 questions**, multiple choice / multiple select
- **Price:** USD $125 + tax
- **Languages:** English, Spanish, Japanese, Portuguese (the new guide applies to
  the English exam first)
- **Format:** online proctored or on-site (Pearson VUE)
- **Valid for:** 3 years — no prerequisites
- **Recommended experience:** 6+ months hands-on with Google Cloud

## CURRENT blueprint (2026-06-30 guide, 4 sections)

### Section 1: Setting up a cloud solution environment (~20%)
- 1.1 Projects and accounts: resource hierarchy, organization policies, IAM
  roles, Cloud Identity, APIs, Observability, quotas, standalone organizations,
  initial networking, region/zone availability, **Cloud Asset Inventory + Gemini
  Cloud Assist**, **Workforce Identity Federation**
- 1.2 Billing: accounts, linking projects, budgets and alerts, exports

### Section 2: Planning and implementing a cloud solution (~30%)
- 2.1 Compute: choosing between Compute Engine, GKE, Cloud Run, **Cloud Run
  functions**, **Agent Runtime on the Gemini Enterprise Agent Platform**;
  instances, disks (zonal/regional PD, **Hyperdisk**), MIGs with autoscaling, OS
  Login, VM Manager, Spot VMs, custom machine types; kubectl, GKE clusters
  (Autopilot, regional, private), container deployment; serverless with events
  (Pub/Sub, Cloud Storage, Eventarc); **GPUs vs TPUs**
- 2.2 Storage and data: Cloud SQL, BigQuery, Firestore, Spanner, Bigtable,
  AlloyDB, Dataflow, Pub/Sub, **Managed Service for Apache Kafka**,
  **Memorystore**; Cloud Storage, **Filestore**, **NetApp Volumes**, **Managed
  Lustre**; storage classes; data loading; multi-region redundancy
- 2.3 Networking: VPC with subnets (custom mode, Shared VPC, VPC Peering),
  firewall rules and **Cloud NGFW** (secure tags, service accounts),
  connectivity (Cloud VPN, Peering, **Cloud Interconnect**), load balancers,
  Network Service Tiers
- 2.4 Tooling: IaC (**Fabric FAST**, Config Connector, Terraform, Helm); **AI
  assistance: Gemini CLI, Google Antigravity, Gemini Cloud Assist, Application
  Design Center**

### Section 3: Ensuring successful operation (~30%)
- 3.1 Compute: remote access, inventory, snapshots/images, GKE inventory,
  Artifact Registry, node pools, K8s resources, HPA/VPA, **Autopilot Pod
  resource requests**, Cloud Run revisions, traffic splitting, Cloud Run
  autoscaling, **GPUs/TPUs**, **deploying agents on Agent Runtime**,
  **notebooks (Workbench / BigQuery)**, **Cloud Workstations**
- 3.2 Data: buckets and lifecycle, queries, cost estimation, backup/restore
  (Cloud SQL, Firestore, Spanner, AlloyDB, Bigtable), job status, **Database
  Center**, **CMEK**
- 3.3 Networking: resizing subnets, static IPs, **custom static routes**, Cloud
  DNS, Cloud NAT, firewall/NGFW rules
- 3.4 Monitoring and logging: alerts, custom metrics, audit logs (**VPC Flow
  Logs, firewall logs**), log exports, log buckets/analytics/routers, Cloud
  Logging, diagnostic tooling (**Cloud Trace, Cloud Profiler, Query Insights,
  index advisor**), **Personalized Service Health**, Ops Agent, Managed Service
  for Prometheus, **Gemini Cloud Assist for Monitoring**, **Active Assist**,
  **Cloud Hub**

### Section 4: Configuring access and security (~20%)
- 4.1 IAM: policies, inheritance across the hierarchy, role types, custom roles
- 4.2 Service accounts: creation (including Google-managed), least privilege,
  assigning them to resources, impersonation, short-lived credentials, **SAs
  with GKE apps**, **Workload Identity Federation**

### Key changes vs. the previous guide (so you neither over- nor under-study)
- Goes from 5 to **4 sections**: "Planning" and "Implementing" merge (~30%), and
  "Operations" rises to ~30%
- **New — AI:** Gemini Cloud Assist, Gemini CLI, Google Antigravity, Agent
  Runtime, GPUs/TPUs, notebooks
- **New — security/networking:** Cloud NGFW, Workforce/Workload Identity
  Federation, CMEK, Cloud Interconnect
- **New — data/storage:** Hyperdisk, Memorystore, Managed Kafka, Filestore,
  NetApp Volumes, Managed Lustre, Database Center
- **New — operations:** Active Assist, Cloud Hub, Personalized Service Health,
  Cloud Trace/Profiler, Cloud Workstations
- Dropped: Deployment Manager / Cloud Foundation Toolkit (replaced by Fabric
  FAST), Cloud Run for Anthos

## Official learning path (priority) — 17 activities

"Associate Cloud Engineer Certification" on Google Skills (~70 h in total):

| # | Type | Activity | Length |
|---|---|---|---|
| 1 | Lab | A tour of Google Cloud hands-on labs | 45 min |
| 2 | Course | Build a study guide for the ACE exam (NotebookLM) | 1 h |
| 3 | Course | Essential Google Cloud Infrastructure: Foundation | 6 h 45 min |
| 4 | Course | Essential Google Cloud Infrastructure: Core Services | 8 h 15 min |
| 5 | Course | Elastic Google Cloud Infrastructure: Scaling and Automation | 7 h |
| 6 | Course | Getting Started with Google Kubernetes Engine | 5 h |
| 7 | Course | Develop applications with Cloud Run: fundamentals | 5 h |
| 8 | Course | Develop applications with Cloud Run Functions | 7 h 15 min |
| 9 | Course | Choose a Google Cloud database | 6 h |
| 10 | Course | AI Infrastructure: Cloud GPUs | 1 h |
| 11 | Course | AI Infrastructure: Cloud TPUs | 1 h 15 min |
| 12 | Course | AI Infrastructure: deployment types | 1 h 30 min |
| 13 | Course | Logging and Monitoring in Google Cloud | 8 h 30 min |
| 14 | Course | Introduction to Terraform for Google Cloud | 6 h 30 min |
| 15 | Skill badge | Implement Cloud Load Balancing for Compute Engine | 30 min |
| 16 | Skill badge | Deploy Kubernetes applications on Google Cloud | 1 h 45 min |
| 17 | Skill badge | Build infrastructure with Terraform on Google Cloud | 1 h 45 min |

Titles follow the official path; check the
[path itself](https://www.skills.google/paths/11) for the exact current wording.

## Third-party write-ups on the refresh (2025-2026)

- [CBT Nuggets — ACE Exam Update: What's Changed in 2025?](https://www.cbtnuggets.com/blog/certifications/cloud/google-associate-cloud-engineer-ace-exam-update-whats-changed-in-2025)
- [3university — Google Cloud Certification Changes 2026](https://www.3university.io/learn/google-cloud-certification-changes/)
- [CertLand — ACE Study Guide 2026](https://certland.net/blog/google-cloud-associate-cloud-engineer-ace-study-guide-2026/)
- [ExamCert — GCP ACE Study Guide 2026](https://www.examcert.app/blog/gcp-ace-study-guide-2026/)
- [ExamTopics — free ACE question bank](https://www.examtopics.com/exams/google/associate-cloud-engineer/) (verify the answers: the community argues over each one)
- [TrustEd Institute — practice by concept, includes new topics such as Gemini Cloud Assist](https://trustedinstitute.com/concept/gcp-associate-cloud-engineer/)
- [Udemy — 2026 ACE Practice Exams](https://www.udemy.com/course/practice-exams-google-associate-cloud-engineer-ace-i/) (paid)
- [Whizlabs — GCP ACE practice tests](https://www.whizlabs.com/blog/gcp-associate-cloud-engineer-exam-questions/) (paid)
- [Google Cloud blog — Preparing for the ACE certification](https://cloud.google.com/blog/topics/training-certifications/preparing-for-the-associate-cloud-engineer-certification)

## Hands-on practice

- Free trial: USD $300 in credits for new users —
  https://console.cloud.google.com/freetrial
- Always-free tier: 20+ products
