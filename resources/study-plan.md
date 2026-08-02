# Study plan — Google Associate Cloud Engineer (10 weeks)

Goal: sit the exam against the current blueprint (guide effective 2026-06-30).
Backbone: the [official learning path](https://www.skills.google/paths/11) (~70 h)
plus the local quiz app (`quiz-app/`).

**Suggested pace:** ~7-8 h/week (courses + labs + quizzes). Adjustable — what
rules is each week's exit criterion, not the calendar.

## When to book the exam

**A consistent ≥90% across 3 back-to-back full mock exams** (50 questions / 2 h).
At that level the margin over the real cut (~70%) absorbs exam-day nerves. Book
at [certmetrics](https://cp.certmetrics.com/google/en/login) about two weeks ahead.

## Week by week

| Week | Learning path courses (Google Skills) | Practice in the app |
|---|---|---|
| 1 | Labs intro (45 min) + Build a study guide with NotebookLM (1 h) + **Essential Infrastructure: Foundation** (6:45) | Quiz by course: foundation (3 levels) |
| 2 | **Essential Infrastructure: Core Services** (8:15) | Quiz by course + quiz by service: IAM, VPC, Compute Engine |
| 3 | **Elastic Infrastructure: Scaling and Automation** (7:00) + **Load Balancing badge** (0:30) | Quiz by course + services: Load Balancing, MIGs/autoscaling |
| 4 | **Getting Started with GKE** (5:00) + **Kubernetes badge** (1:45) | GKE quiz by course + a calibration **short exam** |
| 5 | **Cloud Run: fundamentals** (5:00) + **Cloud Run Functions** (7:15) | Quizzes by course + services: Cloud Run, Eventarc, Pub/Sub |
| 6 | **Choose a database** (6:00) | Quiz by course + services: Cloud SQL, Spanner, Bigtable, Firestore, AlloyDB, Memorystore |
| 7 | **AI: GPUs** (1:00) + **AI: TPUs** (1:15) + **AI: deployment types** (1:30) | AI quizzes + reinforcement by service: Gemini Cloud Assist, Agent Runtime, GPUs/TPUs + a **short exam** |
| 8 | **Logging and Monitoring** (8:30) | Quiz by course + services: Monitoring, Logging, Ops Agent + a **medium exam** |
| 9 | **Intro to Terraform** (6:30) + **Terraform badge** (1:45) | Terraform quiz + **gap reinforcement**: billing, Cloud NGFW, CMEK, Workforce/Workload Identity Federation, Database Center, Active Assist, Cloud Hub (study by service) |
| 10 | Review driven by the dashboard (weakest topics first) | **Full mock exams** every other day plus a review of what you missed; also the [official sample questions](https://docs.google.com/forms/d/e/1FAIpQLSewdU5twM8Y9zY4Z7Syo1M7oikGuKACB_UN5XBRJDlnpAV9Bw/viewform) |

If by week 10 the mock average is still under 90%, extend one or two weeks
repeating the week-10 cycle — the dashboard tells you exactly what to review
(recommended focus).

## Practice rules

1. **Finish a course → take its quiz the same day** (beginner → intermediate →
   advanced levels).
2. **Every missed question gets re-read with its explanation and doc link** — the
   explanation of why the other options fail is where most of the learning is.
3. **Exams are taken in one sitting, with the timer on** — simulate real
   conditions from week 4 onwards.
4. **Check the dashboard every week**: whatever is red or unpracticed defines the
   next session.
5. **Real hands-on**: use your own GCP project (or the
   [free tier](https://console.cloud.google.com/freetrial)) to run the commands
   from intermediate questions you get wrong — muscle memory beats visual memory.

## On exam day

- 2 h / 50-60 questions → ~2 min per question; flag it and move on if one takes
  more than 3 minutes.
- Read the last sentence of the scenario first: that is usually where the real
  question is ("MOST cost-effective?", "LEAST operational effort?", "following
  Google-recommended practices?").
- Discard the absurd options first (wrong product) — you are almost always left
  with two plausible ones, and the difference is a requirement stated in the
  scenario.
