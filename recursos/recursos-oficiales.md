# Recursos oficiales — Google Associate Cloud Engineer (ACE)

Analizados el 2026-08-02.

> ⚠️ **Importante:** El examen se actualizó con una **nueva guía vigente desde el 30 de junio de 2026** (blueprint de 4 secciones). La guía en español de 5 secciones es la versión ANTERIOR. Estudiar según la guía nueva.

## Links

| Recurso | URL |
|---|---|
| **Guía del examen VIGENTE (desde 2026-06-30, inglés)** | https://services.google.com/fh/files/misc/063026_associate_cloud_engineer_exam_guide_english.pdf |
| Guía anterior del examen (español, 5 secciones) | https://services.google.com/fh/files/misc/associate_cloud_engineer_exam_guide_spanish.pdf?hl=es-419 |
| Página de la certificación | https://cloud.google.com/learn/certification/cloud-engineer?hl=es-419 |
| **Learning path oficial (prioridad de estudio)** | https://www.skills.google/paths/11 |
| Preguntas de ejemplo oficiales | https://docs.google.com/forms/d/e/1FAIpQLSewdU5twM8Y9zY4Z7Syo1M7oikGuKACB_UN5XBRJDlnpAV9Bw/viewform |
| Registro del examen | https://cp.certmetrics.com/google/en/login |

Copias locales: [`guia-examen-ace-2026-06-30-en.pdf`](guia-examen-ace-2026-06-30-en.pdf) (vigente) · [`guia-examen-ace-es.pdf`](guia-examen-ace-es.pdf) (anterior)

## Datos del examen

- **Duración:** 2 horas — **50-60 preguntas** de opción múltiple / selección múltiple
- **Costo:** USD $125 + impuestos
- **Idiomas:** español, inglés, japonés, portugués (la guía nueva aplica primero al examen en inglés)
- **Modalidad:** online con supervisión o presencial (Pearson VUE)
- **Vigencia:** 3 años — sin prerrequisitos
- **Experiencia recomendada:** 6+ meses hands-on con Google Cloud

## Blueprint VIGENTE (guía 2026-06-30, 4 secciones)

### Sección 1: Setting up a cloud solution environment (~20%)
- 1.1 Proyectos y cuentas: jerarquía de recursos, políticas de organización, roles IAM, Cloud Identity, APIs, Observability, cuotas, organizaciones standalone, networking inicial, disponibilidad por regiones/zonas, **Cloud Asset Inventory + Gemini Cloud Assist**, **Workforce Identity Federation**
- 1.2 Facturación: cuentas, vincular proyectos, presupuestos y alertas, exportaciones

### Sección 2: Planning and implementing a cloud solution (~30%)
- 2.1 Cómputo: elegir entre Compute Engine, GKE, Cloud Run, **Cloud Run functions**, **Agent Runtime en Gemini Enterprise Agent Platform**; instancias, discos (zonal/regional PD, **Hyperdisk**), MIGs con autoscaling, OS Login, VM Manager, Spot VMs, tipos de máquina personalizados; kubectl, clústeres GKE (Autopilot, regionales, privados), despliegue de contenedores; serverless con eventos (Pub/Sub, Cloud Storage, Eventarc); **GPUs vs TPUs**
- 2.2 Almacenamiento y datos: Cloud SQL, BigQuery, Firestore, Spanner, Bigtable, AlloyDB, Dataflow, Pub/Sub, **Managed Service for Apache Kafka**, **Memorystore**; Cloud Storage, **Filestore**, **NetApp Volumes**, **Managed Lustre**; clases de almacenamiento; carga de datos; redundancia multirregión
- 2.3 Redes: VPC con subredes (modo personalizado, Shared VPC, VPC Peering), reglas de firewall y **Cloud NGFW** (secure Tags, cuentas de servicio), conectividad (Cloud VPN, Peering, **Cloud Interconnect**), balanceadores de carga, Network Service Tiers
- 2.4 Tooling: IaC (**Fabric FAST**, Config Connector, Terraform, Helm); **asistencia con IA: Gemini CLI, Google Antigravity, Gemini Cloud Assist, Application Design Center**

### Sección 3: Ensuring successful operation (~30%)
- 3.1 Cómputo: acceso remoto, inventario, snapshots/imágenes, inventario GKE, Artifact Registry, node pools, recursos K8s, HPA/VPA, **Autopilot Pod resource requests**, versiones Cloud Run, división de tráfico, autoscaling Cloud Run, **GPUs/TPUs**, **desplegar agentes en Agent Runtime**, **notebooks (Workbench/BigQuery)**, **Cloud Workstations**
- 3.2 Datos: buckets y ciclo de vida, consultas, estimación de costos, backups/restore (Cloud SQL, Firestore, Spanner, AlloyDB, Bigtable), estado de jobs, **Database Center**, **CMEK**
- 3.3 Redes: redimensionar subredes, IPs estáticas, **rutas estáticas personalizadas**, Cloud DNS, Cloud NAT, reglas firewall/NGFW
- 3.4 Monitoring y logging: alertas, métricas personalizadas, audit logs (**VPC Flow Logs, firewall logs**), exportar logs, log buckets/analytics/routers, Cloud Logging, herramientas de diagnóstico (**Cloud Trace, Cloud Profiler, Query Insights, index advisor**), **Personalized Service Health**, Ops Agent, Managed Service for Prometheus, **Gemini Cloud Assist para Monitoring**, **Active Assist**, **Cloud Hub**

### Sección 4: Configuring access and security (~20%)
- 4.1 IAM: políticas, herencia en la jerarquía, tipos de roles, roles personalizados
- 4.2 Cuentas de servicio: creación (incl. Google-managed), mínimo privilegio, asignación a recursos, impersonación, credenciales de corta duración, **SA con apps GKE**, **Workload Identity Federation**

### Cambios clave vs. guía anterior (para no estudiar de más ni de menos)
- Pasa de 5 a **4 secciones**: "Planning" e "Implementing" se fusionan (~30%), "Operations" sube a ~30%
- **Nuevo — IA:** Gemini Cloud Assist, Gemini CLI, Google Antigravity, Agent Runtime, GPUs/TPUs, notebooks
- **Nuevo — seguridad/redes:** Cloud NGFW, Workforce/Workload Identity Federation, CMEK, Cloud Interconnect
- **Nuevo — datos/storage:** Hyperdisk, Memorystore, Managed Kafka, Filestore, NetApp Volumes, Managed Lustre, Database Center
- **Nuevo — operaciones:** Active Assist, Cloud Hub, Personalized Service Health, Cloud Trace/Profiler, Cloud Workstations
- Sale: Deployment Manager / Cloud Foundation Toolkit (reemplazado por Fabric FAST), Cloud Run for Anthos

## Learning path oficial (prioridad) — 17 actividades

"Associate Cloud Engineer Certification" en Google Skills (~70 h en total):

| # | Tipo | Actividad | Duración |
|---|---|---|---|
| 1 | Lab | Recorrido por los labs prácticos de Google Cloud | 45 min |
| 2 | Curso | Crea una guía de estudio para el examen ACE (NotebookLM) | 1 h |
| 3 | Curso | Infraestructura esencial de Google Cloud: conceptos básicos | 6 h 45 min |
| 4 | Curso | Infraestructura esencial de Google Cloud: servicios principales | 8 h 15 min |
| 5 | Curso | Infraestructura elástica de Google Cloud: escalamiento y automatización | 7 h |
| 6 | Curso | Cómo comenzar a usar Google Kubernetes Engine | 5 h |
| 7 | Curso | Desarrolla aplicaciones con Cloud Run: conceptos básicos | 5 h |
| 8 | Curso | Desarrolla aplicaciones con Cloud Run Functions | 7 h 15 min |
| 9 | Curso | Selecciona una base de datos de Google Cloud | 6 h |
| 10 | Curso | Infraestructura de IA: GPU de Cloud | 1 h |
| 11 | Curso | Infraestructura de IA: TPU de Cloud | 1 h 15 min |
| 12 | Curso | Infraestructura de IA: tipos de implementación | 1 h 30 min |
| 13 | Curso | Registro y supervisión en Google Cloud | 8 h 30 min |
| 14 | Curso | Introducción a Terraform para Google Cloud | 6 h 30 min |
| 15 | Skill badge | Implementa Cloud Load Balancing para Compute Engine | 30 min |
| 16 | Skill badge | Implementa aplicaciones de Kubernetes en Google Cloud | 1 h 45 min |
| 17 | Skill badge | Crea una infraestructura con Terraform en Google Cloud | 1 h 45 min |

## Fuentes actualizadas (2025-2026)

- [CBT Nuggets — ACE Exam Update: What's Changed in 2025?](https://www.cbtnuggets.com/blog/certifications/cloud/google-associate-cloud-engineer-ace-exam-update-whats-changed-in-2025) — análisis del refresh del blueprint
- [3university — Google Cloud Certification Changes 2026](https://www.3university.io/learn/google-cloud-certification-changes/)
- [CertLand — ACE Study Guide 2026](https://certland.net/blog/google-cloud-associate-cloud-engineer-ace-study-guide-2026/)
- [ExamCert — GCP ACE Study Guide 2026](https://www.examcert.app/blog/gcp-ace-study-guide-2026/)
- [ExamTopics — banco de preguntas gratuito ACE](https://www.examtopics.com/exams/google/associate-cloud-engineer/) (verificar respuestas: la comunidad discute cada una)
- [TrustEd Institute — práctica por concepto, incluye temas nuevos como Gemini Cloud Assist](https://trustedinstitute.com/concept/gcp-associate-cloud-engineer/)
- [Udemy — 2026 Practice Exams ACE](https://www.udemy.com/course/practice-exams-google-associate-cloud-engineer-ace-i/) (de pago)
- [Whizlabs — GCP ACE practice tests](https://www.whizlabs.com/blog/gcp-associate-cloud-engineer-exam-questions/) (de pago)
- [Blog oficial de Google Cloud — Preparing for the ACE certification](https://cloud.google.com/blog/topics/training-certifications/preparing-for-the-associate-cloud-engineer-certification)

## Práctica hands-on

- Free trial: USD $300 en créditos para usuarios nuevos — https://console.cloud.google.com/freetrial
- Free tier permanente: 20+ productos
