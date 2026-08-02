# Plan de estudio — Google Associate Cloud Engineer (10 semanas)

Objetivo: presentar el examen en **octubre-noviembre 2026** con el blueprint vigente (guía 2026-06-30). Columna vertebral: el [learning path oficial](https://www.skills.google/paths/11) (~70 h) + la app de quizzes local (`quiz-app/`).

**Ritmo sugerido:** ~7-8 h/semana (cursos + labs + quizzes). Ajustable: lo que manda es el criterio de salida de cada semana, no el calendario.

## Criterio para agendar el examen

**≥90% consistente en 3 simulacros full seguidos** (50 preguntas / 2 h). Con eso, el margen sobre el corte real (~70%) absorbe los nervios del día del examen. Agenda en [certmetrics](https://cp.certmetrics.com/google/en/login) con ~2 semanas de anticipación.

## Semana a semana

| Semana | Cursos del path (Google Skills) | Práctica en la app |
|---|---|---|
| 1 | Lab intro (45 min) + Crea una guía de estudio con NotebookLM (1 h) + **Infraestructura esencial: conceptos básicos** (6:45) | Quiz por curso: `conceptos básicos` (3 niveles) |
| 2 | **Infraestructura esencial: servicios principales** (8:15) | Quiz por curso + quiz por servicio: IAM, VPC, Compute Engine |
| 3 | **Infraestructura elástica: escalamiento y automatización** (7:00) + **badge Load Balancing** (0:30) | Quiz por curso + servicios: Load Balancing, MIGs/autoscaling |
| 4 | **Cómo comenzar a usar GKE** (5:00) + **badge Kubernetes** (1:45) | Quiz por curso GKE + **examen corto** de calibración |
| 5 | **Cloud Run: conceptos básicos** (5:00) + **Cloud Run Functions** (7:15) | Quizzes por curso + servicios: Cloud Run, Eventarc, Pub/Sub |
| 6 | **Selecciona una base de datos** (6:00) | Quiz por curso + servicios: Cloud SQL, Spanner, Bigtable, Firestore, AlloyDB, Memorystore |
| 7 | **IA: GPU** (1:00) + **IA: TPU** (1:15) + **IA: implementación** (1:30) | Quizzes IA + refuerzo por servicio: Gemini Cloud Assist, Agent Runtime, GPUs/TPUs + **examen corto** |
| 8 | **Registro y supervisión** (8:30) | Quiz por curso + servicios: Monitoring, Logging, Ops Agent + **examen medio** |
| 9 | **Intro a Terraform** (6:30) + **badge Terraform** (1:45) | Quiz Terraform + **refuerzo de huecos**: facturación, Cloud NGFW, CMEK, Workforce/Workload Identity Federation, Database Center, Active Assist, Cloud Hub (estudiar por servicio) |
| 10 | Repaso dirigido por el dashboard (semáforo débil primero) | **Simulacros full** día por medio + revisión de falladas; también las [preguntas de ejemplo oficiales](https://docs.google.com/forms/d/e/1FAIpQLSewdU5twM8Y9zY4Z7Syo1M7oikGuKACB_UN5XBRJDlnpAV9Bw/viewform) |

Si a la semana 10 el promedio de simulacros está bajo 90%, extiende 1-2 semanas repitiendo el ciclo de la semana 10 — el dashboard te dice exactamente qué repasar (enfoque recomendado).

## Reglas de práctica

1. **Termina cada curso → quiz por curso el mismo día** (niveles principiante → intermedio → avanzado).
2. **Toda pregunta fallada se relee con su explicación y el link a la doc** — la explicación de por qué las otras opciones fallan es donde más se aprende.
3. **Los exámenes se hacen sin pausa y con temporizador** — simular condiciones reales desde la semana 4.
4. **Revisa el dashboard cada semana**: los temas en rojo/sin practicar definen la sesión siguiente.
5. **Hands-on real**: usa tu proyecto GCP (o el [free tier](https://console.cloud.google.com/freetrial)) para ejecutar los comandos que aparezcan en preguntas intermedias que falles — memoria muscular > memoria visual.

## El día del examen

- 2 h / 50-60 preguntas → ~2 min por pregunta; marca y sigue si dudas más de 3 min.
- Lee la última frase del escenario primero: ahí suele estar la pregunta real ("¿MÁS económico?", "¿MENOS esfuerzo operativo?", "¿siguiendo las prácticas recomendadas de Google?").
- Descarta primero las opciones absurdas (producto equivocado) — casi siempre quedan 2 plausibles y la diferencia es un requisito del escenario.
