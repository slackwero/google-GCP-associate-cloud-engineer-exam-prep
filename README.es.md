# Google Cloud Platform (GCP) - Associate Cloud Engineer — Preparación para el examen

![plataforma](https://img.shields.io/badge/plataforma-Linux%20%7C%20macOS-blue)
![python](https://img.shields.io/badge/python-%E2%89%A53.10-green)
![preguntas](https://img.shields.io/badge/preguntas-1%2C465-blue)
![licencia](https://img.shields.io/badge/licencia-MIT-lightgrey)

> [!IMPORTANT]
> **Esto es práctica para el examen, no un curso.** Todo aquí gira en torno a
> **preguntas tipo examen** para la certificación **Google Cloud Associate Cloud
> Engineer**: 1.465 preguntas bilingües (inglés / español latinoamericano),
> simulacros cronometrados y un dashboard de avances que te mide contra la guía
> oficial. Practicas preguntas hasta que el puntaje diga que estás listo.

Todo corre en tu máquina. Sin cuentas, sin servidor, sin telemetría — tu
historial de estudio es un archivo en tu disco.

> **No está afiliado a Google.** Es un proyecto de estudio independiente.
> "Google Cloud" y "Associate Cloud Engineer" son marcas de Google LLC,
> referenciadas aquí de forma descriptiva.

🇬🇧 [Read this in English](README.md)

---

## Qué incluye

- **1.465 preguntas bilingües**, todas mapeadas al blueprint oficial del examen.
  Cada una explica por qué la respuesta correcta lo es **y por qué falla cada
  distractor**, con enlace a la documentación oficial.
- **100% de cobertura del blueprint** — los 70 subtópicos de la guía vigente
  desde el **2026-06-30** (4 secciones, pesos 20/30/30/20).
- **Modo de práctica** por curso (las 15 actividades del path oficial) o por
  servicio de Google Cloud, con feedback inmediato.
- **Simulacros cronometrados**: 20 preguntas / 25 min, 40 / 50 min, y uno
  completo de 50 / 2 h que muestrea según los pesos reales de cada sección.
- **Dashboard de avances**: dominio por sección, servicio y curso, cobertura del
  banco, evolución del puntaje y un enfoque recomendado que te dice qué estudiar
  a continuación.
- **Inglés y español en el mismo registro** de pregunta — puedes cambiar de
  idioma en cualquier momento, incluso a mitad de un examen.

## Requisitos

**Python 3.10 o superior.** Nada más.

**No** hace falta instalar Node, y **no** hace falta instalar un motor de base de
datos. Reflex descarga su propio runtime de JavaScript en el primer arranque, y
la app guarda tu historial en SQLite, que viene dentro de la biblioteca estándar
de Python.

## Cómo arrancar

```bash
git clone git@github.com:slackwero/google-GCP-associate-cloud-engineer-exam-prep.git
cd google-GCP-associate-cloud-engineer-exam-prep

./run.sh
```

Luego abre <http://localhost:3000>. Con `Ctrl+C` detienes la app.

Esa es toda la instalación. La primera vez, `run.sh` crea un entorno de Python
aislado e instala ahí las dependencias; a partir de entonces solo levanta la app.
Vuelve a instalar por su cuenta únicamente si las dependencias cambian, y nunca
toca los paquetes de Python del resto de tu sistema.

Dos cosas que conviene saber:

- **El primer arranque tarda** (un minuto o más). Reflex está descargando su
  runtime de JavaScript y compilando el frontend. Los siguientes son rápidos.
- **Solo necesitas internet para instalar.** Una vez configurada, la app funciona
  sin conexión: el banco de preguntas y las fuentes están en el repositorio.

La base de datos se crea sola en el primer arranque. Empiezas con el historial
vacío y el banco de preguntas completo.

Si la app ya está corriendo y los puertos 3000/8000 están ocupados, reemplázala
con:

```bash
./run.sh --restart
```

`./run.sh --reinstall` reconstruye el entorno desde cero, por si alguna vez queda
en mal estado.

## Qué cubre

Cada pregunta lleva etiquetada la sección y el subtópico del examen al que
pertenece, y el banco está repartido según los pesos de la guía oficial — así un
simulacro completo se siente como el examen real y no como lo que era más fácil
de escribir.

| Sección del examen | Peso | Preguntas | Subtópicos |
|---|---|---|---|
| 1. Configuración de un entorno de solución en la nube | 20% | 211 | 11 |
| 2. Planificación e implementación de una solución en la nube | 30% | 606 | 21 |
| 3. Cómo asegurar la operación exitosa de una solución en la nube | 30% | 429 | 29 |
| 4. Configuración del acceso y la seguridad | 20% | 219 | 9 |
| **Total** | **100%** | **1.465** | **70** |

Puedes practicar por tema del examen, por curso del learning path oficial (15
actividades) o por servicio. Estos son los 52 servicios y áreas por los que está
indexado el banco:

**Cómputo y contenedores** — Compute Engine · Google Kubernetes Engine (GKE) ·
Cloud Run · Cloud Run functions · Persistent Disk / Hyperdisk · Artifact
Registry · kubectl / Kubernetes CLI · Helm · Eventarc

**Almacenamiento y datos** — Cloud Storage · Cloud SQL · AlloyDB · Spanner ·
Firestore · Bigtable · BigQuery · Memorystore · Filestore / NetApp Volumes /
Managed Lustre · Dataflow · Pub/Sub · Managed Service for Apache Kafka ·
Storage Transfer Service · Database Center

**Redes** — VPC / Networking · Cloud Load Balancing · Cloud DNS · Cloud NAT ·
Cloud NGFW / Firewall · Cloud VPN / Interconnect · Network Service Tiers

**Operación y observabilidad** — Cloud Monitoring · Cloud Logging · Ops Agent /
Managed Prometheus · Cloud Trace / Profiler / diagnostics · Active Assist /
Recommender · Cloud Hub / Service Health · Cloud Asset Inventory

**Identidad y seguridad** — IAM · Service accounts · Cloud Identity · Resource
hierarchy / Organization · Workforce / Workload Identity Federation · CMEK /
Cloud KMS

**Facturación y gobierno** — Cloud Billing · APIs / Quotas

**IA y herramientas** — Gemini Cloud Assist / Gemini CLI · Agent Runtime (Gemini
Enterprise Agent Platform) · GPUs / TPUs · Notebooks (Workbench / BigQuery) ·
Cloud Workstations · Terraform / IaC · gcloud CLI / Cloud Shell

Un test de la suite falla si algún subtópico baja de cinco preguntas, así que la
cobertura de arriba se verifica en cada cambio en vez de solo prometerse aquí.

## Dónde se guardan los datos

| | Dónde | ¿Versionado en git? |
|---|---|---|
| **Banco de preguntas, cursos, servicios, blueprint** | Archivos JSON en `quiz-app/data/` | Sí |
| **Tus intentos y respuestas** | SQLite en `quiz-app/quiz_ace.db` | **No** |

El contenido se versiona como si fuera código: se revisa en diffs y lo valida la
suite de tests. Tu progreso es tuyo y nunca sale de tu máquina — borrar
`quiz_ace.db` reinicia tu historial y nada más.

## Licencia

[MIT](LICENSE) — tanto el código como el banco de preguntas. Úsalo, forkéalo,
construye sobre él, incluso comercialmente; solo conserva el aviso de copyright.

Los archivos de la fuente Roboto son un caso aparte: se distribuyen bajo la
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), como documenta
[`quiz-app/assets/fonts/README.md`](quiz-app/assets/fonts/README.md).
