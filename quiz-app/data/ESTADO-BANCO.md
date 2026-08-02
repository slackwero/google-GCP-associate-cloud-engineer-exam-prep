# Estado del banco de preguntas

Actualizar esta tabla cada vez que se complete un archivo. Meta total: **~1,200 preguntas**.

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

| Archivo | Prefijo id | Meta | Temas |
|---|---|---|---|
| `infraestructura-conceptos-basicos.json` | `fund` | 65 | Jerarquía, IAM, facturación, cuotas, panorama de servicios |
| `infraestructura-servicios-principales.json` | `infra` | 65 | VPC a fondo, Compute Engine, discos, snapshots, Cloud Storage |
| `infraestructura-escalamiento-automatizacion.json` | `elas` | 65 | Load balancing, MIGs, VPN/Interconnect, Shared VPC, NAT |
| `como-comenzar-gke.json` | `gke` | 65 | GKE completo: clústeres, Pods, node pools, autoscaling |
| `cloud-run-conceptos-basicos.json` | `run` | 65 | Cloud Run: revisiones, tráfico, concurrencia, escalado |
| `cloud-run-functions.json` | `crf` | 65 | Functions, Eventarc, Pub/Sub, eventos de Storage |
| `selecciona-base-de-datos.json` | `db` | 65 | Cloud SQL, AlloyDB, Spanner, Firestore, Bigtable, BigQuery |
| `ia-gpu.json` | `gpu` | 60 | GPUs en Compute/GKE/Cloud Run, cuotas, Spot |
| `ia-tpu.json` | `tpu` | 60 | TPUs, cuándo vs GPU, frameworks, costos |
| `ia-tipos-implementacion.json` | `iadep` | 60 | Agent Runtime, Workbench, Workstations, Lustre |
| `registro-supervision.json` | `ops` | 65 | Monitoring, Logging, audit logs, Ops Agent, diagnóstico |
| `introduccion-terraform.json` | `tf` | 65 | Terraform, Config Connector, Helm, Fabric FAST, Gemini CLI |
| `badge-load-balancing.json` | `lb` | 60 | Lab práctico de balanceadores y health checks |
| `badge-kubernetes-apps.json` | `k8s` | 60 | Lab práctico: Docker, Artifact Registry, despliegue en GKE |
| `badge-terraform-infra.json` | `tfi` | 60 | Lab práctico: recursos, módulos, backend GCS, import |

## Archivos de refuerzo (`"curso": null`)

Cubren temas de la guía oficial que el path NO cubre (ver `recursos/analisis-cobertura.md`).

| Archivo | Prefijo | Meta | Temas |
|---|---|---|---|
| `refuerzo-seccion-1.json` | `ref1` | 70 | Asset Inventory, Gemini Cloud Assist, Workforce Identity Federation, facturación a fondo, cuotas |
| `refuerzo-seccion-2.json` | `ref2` | 80 | Cloud NGFW, Hyperdisk, Memorystore, Kafka, Filestore/NetApp/Lustre, Interconnect |
| `refuerzo-seccion-3.json` | `ref3` | 80 | Database Center, CMEK, costos, rutas estáticas, Trace/Profiler, Workstations, DNS/NAT |
| `refuerzo-seccion-4.json` | `ref4` | 70 | Impersonación, credenciales de corta duración, Workload Identity Federation, herencia IAM, roles personalizados |

## Cierre de la Fase 4

Cuando el banco esté completo, quitar los marcadores `@pytest.mark.xfail` de
`tests/test_cobertura.py` y confirmar que pasa: exige ≥5 preguntas por subtópico
oficial, ≥60 por curso y ≥1,200 en total.
