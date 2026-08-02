# Estado del banco de preguntas

**Banco completo.** El quality gate de cobertura está activo en `tests/test_cobertura.py`
(sin `xfail`): exige ≥5 preguntas por cada subtópico oficial del blueprint 2026,
≥60 por curso del path, ≥1,200 en total y los tres niveles bien representados.

Comando para ver el estado real en cualquier momento:

```bash
cd quiz-app && .venv/bin/python -c "
from pathlib import Path
from quiz_ace.services.banco import cargar_banco, cargar_catalogos
b=cargar_banco(Path('data')); c=cargar_catalogos(Path('data'))
print('VÁLIDAS:', len(b.preguntas), ' EXCLUIDAS:', len(b.excluidas))
for slug in c.cursos: print(f'  {slug:45s} {len(b.por_curso.get(slug,[])):3d}')
print('  refuerzo (curso null):', sum(1 for p in b.preguntas if not p.get('curso')))
" 2>/dev/null
```

## Archivos por curso del path (15)

| Archivo | Prefijo id | Temas |
|---|---|---|
| `infraestructura-conceptos-basicos.json` | `fund` | Jerarquía, IAM, facturación, cuotas, panorama de servicios |
| `infraestructura-servicios-principales.json` | `infra` | VPC a fondo, Compute Engine, discos, snapshots, Cloud Storage |
| `infraestructura-escalamiento-automatizacion.json` | `elas` | Load balancing, MIGs, VPN/Interconnect, Shared VPC, NAT |
| `como-comenzar-gke.json` | `gke` | GKE completo: clústeres, Pods, node pools, autoscaling |
| `cloud-run-conceptos-basicos.json` | `run` | Cloud Run: revisiones, tráfico, concurrencia, escalado |
| `cloud-run-functions.json` | `crf` | Functions, Eventarc, Pub/Sub, eventos de Storage |
| `selecciona-base-de-datos.json` | `db` | Cloud SQL, AlloyDB, Spanner, Firestore, Bigtable, BigQuery |
| `ia-gpu.json` | `gpu` | GPUs en Compute/GKE/Cloud Run, cuotas, Spot |
| `ia-tpu.json` | `tpu` | TPUs, cuándo vs GPU, frameworks, costos |
| `ia-tipos-implementacion.json` | `iadep` | Agent Runtime, Workbench, Workstations, Lustre |
| `registro-supervision.json` | `ops` | Monitoring, Logging, audit logs, Ops Agent, diagnóstico |
| `introduccion-terraform.json` | `tf` | Terraform, Config Connector, Helm, Fabric FAST, Gemini CLI |
| `badge-load-balancing.json` | `lb` | Lab práctico de balanceadores y health checks |
| `badge-kubernetes-apps.json` | `k8s` | Lab práctico: Docker, Artifact Registry, despliegue en GKE |
| `badge-terraform-infra.json` | `tfi` | Lab práctico: recursos, módulos, backend GCS, import |

## Archivos de refuerzo (`"curso": null`)

Cubren temas de la guía oficial que el path NO cubre (ver `recursos/analisis-cobertura.md`).

| Archivo | Prefijo | Temas |
|---|---|---|
| `refuerzo-seccion-1.json` | `ref1` | Asset Inventory, Gemini Cloud Assist, Workforce Identity Federation, facturación a fondo, cuotas |
| `refuerzo-seccion-1b.json` | `s1b` | Más Sección 1: equilibra el peso real del examen (20%) |
| `refuerzo-seccion-2.json` | `ref2` | Cloud NGFW, Hyperdisk, Memorystore, Kafka, Filestore/NetApp/Lustre, Interconnect |
| `refuerzo-seccion-3.json` | `ref3` | Database Center, CMEK, costos, rutas estáticas, Trace/Profiler, Workstations, DNS/NAT |
| `refuerzo-seccion-4.json` | `ref4` | Impersonación, credenciales de corta duración, Workload Identity Federation, herencia IAM, roles personalizados |
| `refuerzo-cobertura.json` | `cob` | Cierra subtópicos con poca cobertura: secure Tags en NGFW, operación de instancias, estado de jobs, Gemini Cloud Assist, Active Assist |

## Si quieres ampliar el banco

Añade un archivo nuevo en `data/preguntas/` siguiendo el esquema (usa
`como-comenzar-gke.json` como referencia de calidad) y ejecuta `pytest`: el
validador rechaza cualquier pregunta mal formada y el gate confirma la cobertura.
Las Secciones 1 y 4 son las que más ganarían con más preguntas: pesan 20% cada una
en el examen y siguen siendo las de menor volumen en el banco.
