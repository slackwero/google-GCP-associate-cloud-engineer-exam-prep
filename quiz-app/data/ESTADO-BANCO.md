# Estado del banco de preguntas

**Banco completo: 1,516 preguntas bilingües, 0 excluidas.** El quality gate de cobertura
está activo en `tests/test_cobertura.py` (sin `xfail`): exige ≥5 preguntas por cada
subtópico oficial del blueprint 2026, ≥60 por curso del path, ≥1,200 en total y los
tres niveles bien representados.

Distribución verificada: 461 principiante / 543 intermedio / 512 avanzado.
Por sección del examen: S1 213, S2 613, S3 471, S4 219.
Ningún subtópico oficial baja de 12 preguntas.

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

Cubren temas de la guía oficial que el path NO cubre (ver `resources/coverage-analysis.md`).

| Archivo | Prefijo | Temas |
|---|---|---|
| `refuerzo-seccion-1.json` | `ref1` | Asset Inventory, Gemini Cloud Assist, Workforce Identity Federation, facturación a fondo, cuotas |
| `refuerzo-seccion-1b.json` | `s1b` | Más Sección 1: equilibra el peso real del examen (20%) |
| `refuerzo-seccion-2.json` | `ref2` | Cloud NGFW, Hyperdisk, Memorystore, Kafka, Filestore/NetApp/Lustre, Interconnect |
| `refuerzo-seccion-3.json` | `ref3` | Database Center, CMEK, costos, rutas estáticas, Trace/Profiler, Workstations, DNS/NAT |
| `refuerzo-seccion-4.json` | `ref4` | Impersonación, credenciales de corta duración, Workload Identity Federation, herencia IAM, roles personalizados |
| `refuerzo-cobertura.json` | `cob` | Cierra subtópicos con poca cobertura: secure Tags en NGFW, operación de instancias, estado de jobs, Gemini Cloud Assist, Active Assist |
| `refuerzo-densidad.json` | `den` | Sube a 12 los subtópicos más delgados: niveles de red, autoescalado de Pods, instantáneas e imágenes, rutas estáticas, firewall, Ops Agent y Managed Service for Prometheus, logs y Personalized Service Health / Cloud Hub |

## Si quieres ampliar el banco

Añade un archivo nuevo en `data/preguntas/` siguiendo el esquema (usa
`como-comenzar-gke.json` como referencia de calidad) y ejecuta `pytest`: el
validador rechaza cualquier pregunta mal formada y el gate confirma la cobertura.

Para decidir **dónde** ampliar, mide la densidad por subtópico, no el porcentaje por
sección. El reparto bruto engaña: la Sección 1 tiene 11 subtópicos y la 4 solo 9, así
que pesan poco en el total aunque cada subtópico esté bien cubierto (mediana 17 y 26
preguntas). La Sección 3 concentra 29 subtópicos y es la de menor profundidad por
subtópico. Además, el examen simulado ya reparte 20/30/30/20 por sección sin importar
el tamaño del banco, así que la repetición que nota quien estudia viene de los
subtópicos delgados, no del porcentaje de su sección.

```bash
cd quiz-app && .venv/bin/python -c "
import collections
from pathlib import Path
from quiz_ace.services.banco import cargar_banco
b = cargar_banco(Path('data'))
cnt = collections.Counter()
for p in b.preguntas:
    for st in p['subtopicos']: cnt[st] += 1
for st, n in sorted(cnt.items(), key=lambda kv: kv[1])[:15]: print(f'{n:3d}  {st}')
" 2>/dev/null
```
