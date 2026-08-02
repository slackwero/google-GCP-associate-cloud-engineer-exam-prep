# Análisis de cobertura: blueprint 2026 vs path oficial

Fecha: 2026-08-02. Cruce entre la guía oficial vigente del examen (2026-06-30, 4 secciones) y las 17 actividades del learning path oficial (skills.google/paths/11). Este análisis origina los archivos de refuerzo del banco de preguntas.

## Validación de concordancia

- El path oficial **ya está alineado al examen nuevo**: incluye los 3 cursos de Infraestructura de IA (GPU/TPU/tipos de implementación) que corresponden a los temas de IA agregados en la guía 2026, y fue actualizado recientemente.
- La guía en español de 5 secciones es la versión **anterior** — solo referencia histórica.

## Cubierto bien por el path (~70% del blueprint)

| Tema del blueprint | Actividad del path |
|---|---|
| IAM, proyectos, jerarquía, APIs (S1) | Infraestructura esencial: conceptos básicos |
| Compute Engine, discos, VPC, Load Balancing (S2/S3) | Esencial: servicios principales + Elástica + badge LB |
| MIGs, autoscaling, Spot VMs (S2) | Infraestructura elástica |
| GKE: clústeres, kubectl, node pools, HPA/VPA (S2/S3) | Cómo comenzar a usar GKE + badge Kubernetes |
| Cloud Run / Cloud Run functions, Eventarc, eventos (S2/S3) | 2 cursos de Cloud Run |
| Elección de BDs: Cloud SQL, AlloyDB, Spanner, Firestore, Bigtable (S2) | Selecciona una base de datos |
| GPUs vs TPUs, implementación de IA (S2/S3) | 3 cursos de Infraestructura de IA |
| Monitoring, Logging, Ops Agent, Prometheus (S3.4) | Registro y supervisión |
| Terraform, IaC (S2.4) | Intro a Terraform + badge Terraform |

## Huecos del path → archivos de refuerzo del banco

Subtópicos presentes en la guía oficial pero ausentes o superficiales en el path:

### Sección 1 (~20%)
- Facturación a fondo: presupuestos, alertas, exportaciones a BigQuery
- Políticas de organización, organizaciones standalone
- Cloud Identity (gestión de usuarios/grupos), cuotas y aumentos
- **Cloud Asset Inventory + Gemini Cloud Assist para análisis de recursos**
- **Workforce Identity Federation**

### Sección 2 (~30%)
- **Hyperdisk** (vs PD zonal/regional)
- **Agent Runtime en Gemini Enterprise Agent Platform**
- **Memorystore, Managed Service for Apache Kafka, Dataflow**
- **Filestore, NetApp Volumes, Managed Lustre**
- Redundancia multirregión en soluciones de datos
- **Cloud NGFW**: políticas, secure Tags, cuentas de servicio en reglas
- **Cloud Interconnect**, Network Service Tiers
- **Fabric FAST, Config Connector, Helm**
- **Gemini CLI, Google Antigravity, Application Design Center**

### Sección 3 (~30%)
- **Database Center**, **CMEK**
- Estimación de costos de almacenamiento
- Rutas estáticas personalizadas
- **Cloud Trace, Cloud Profiler, Query Insights, index advisor**
- **Active Assist**, **Cloud Hub**, **Personalized Service Health**
- **Cloud Workstations**, notebooks (Workbench / BigQuery)
- Audit logs, VPC Flow Logs, firewall logs

### Sección 4 (~20%)
- Impersonación de cuentas de servicio y credenciales de corta duración
- **Cuentas de servicio con apps GKE + Workload Identity Federation**
- Herencia de políticas IAM en la jerarquía de la organización

## Mitigación en la herramienta

1. `data/blueprint.json` con los ~60 subtópicos oficiales; cada pregunta etiquetada con subtópico.
2. **Test de cobertura**: pytest falla si algún subtópico tiene <5 preguntas → cobertura del 100% del blueprint verificada, no prometida.
3. 250-300 preguntas de refuerzo dedicadas a los huecos listados (banco total ~1,200).
4. Dashboard con cobertura por subtópico y doble meta (70% corte / 95% personal).

## Criterio de "listo para el examen"

≥90% consistente en simulacros full (50 preguntas, 2 h, pesos 20/30/30/20) durante la recta final.
