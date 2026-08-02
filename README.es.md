# Google Cloud Associate Cloud Engineer — Preparación para el examen

Una app local y bilingüe (inglés / español latinoamericano) para preparar la
certificación **Google Cloud Associate Cloud Engineer**: 1.465 preguntas tipo
examen, simulacros cronometrados y un dashboard de avances que te mide contra la
guía oficial.

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
- **100% de cobertura del blueprint** — los 68 subtópicos de la guía vigente
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
cd google-GCP-associate-cloud-engineer-exam-prep/quiz-app

python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

.venv/bin/reflex run
```

Luego abre <http://localhost:3000>.

Dos cosas que conviene saber:

- **El primer arranque tarda** (un minuto o más). Reflex está descargando su
  runtime de JavaScript y compilando el frontend. Los siguientes son rápidos.
- **Solo necesitas internet para instalar.** Una vez configurada, la app funciona
  sin conexión: el banco de preguntas y las fuentes están en el repositorio.

La base de datos se crea sola en el primer arranque. Empiezas con el historial
vacío y el banco de preguntas completo.

Si los puertos 3000/8000 quedaron ocupados de una sesión previa:

```bash
lsof -ti:3000,8000 | xargs kill -9
```

## Dónde se guardan los datos

| | Dónde | ¿Versionado en git? |
|---|---|---|
| **Banco de preguntas, cursos, servicios, blueprint** | Archivos JSON en `quiz-app/data/` | Sí |
| **Tus intentos y respuestas** | SQLite en `quiz-app/quiz_ace.db` | **No** |

El contenido se versiona como si fuera código: se revisa en diffs y lo valida la
suite de tests. Tu progreso es tuyo y nunca sale de tu máquina — borrar
`quiz_ace.db` reinicia tu historial y nada más.

## Desarrollo

```bash
cd quiz-app
.venv/bin/pip install -r requirements-dev.txt

.venv/bin/pytest          # 57 tests, incluido el quality gate de cobertura
.venv/bin/ruff check .    # lint
```

Los tests validan el propio banco de preguntas: esquema, campos bilingües, mapeo
al blueprint y cobertura mínima por subtópico y por curso. Una pregunta inválida
se excluye con un warning en vez de romper la app.

## Estructura del proyecto

```
quiz-app/
  data/                 banco de preguntas + catálogos (JSON, bilingüe)
  quiz_ace/
    services/           lógica en Python puro, sin Reflex — es lo que cubren los tests
    states/             estado de Reflex (idioma, quiz, examen, avances)
    components/         primitivas de UI y piezas compartidas
    pages/              las 7 rutas
  assets/theme.css      el sistema de diseño: cada token de color, forma y movimiento
recursos/               guías oficiales del examen, análisis de cobertura, plan de estudio
```

## Licencia

**Aún sin decidir.** Mientras no exista un archivo de licencia, aplica el
copyright por defecto y no se conceden derechos de reutilización.

Los archivos de la fuente Roboto son un caso aparte: se distribuyen bajo la
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), como documenta
[`quiz-app/assets/fonts/README.md`](quiz-app/assets/fonts/README.md).
