# Google Cloud Associate Cloud Engineer — Certification Exam Prep

A local, bilingual (English / Latin American Spanish) practice app for the
**Google Cloud Associate Cloud Engineer** certification: 1,465 exam-style
questions, timed mock exams, and a progress dashboard that measures you against
the official exam guide.

Everything runs on your machine. No accounts, no server, no telemetry — your
study history is a file on your disk.

> **Not affiliated with Google.** This is an independent study project.
> "Google Cloud" and "Associate Cloud Engineer" are trademarks of Google LLC,
> referenced here descriptively.

🇪🇸 [Léeme en español](README.es.md)

---

## What's inside

- **1,465 bilingual questions**, every one of them mapped to the official exam
  blueprint. Each question explains why the correct answer is correct **and why
  each distractor fails**, with a link to the official documentation.
- **100% blueprint coverage** — all 68 sub-topics of the guide effective
  **2026-06-30** (4 sections, weights 20/30/30/20).
- **Practice mode** by course (the 15 activities of the official learning path)
  or by Google Cloud service, with instant feedback.
- **Timed mock exams**: 20 questions / 25 min, 40 / 50 min, and a full 50 / 2 h
  that samples according to the real section weights.
- **Progress dashboard**: mastery by section, service and course, bank coverage,
  score history, and a recommended focus telling you what to study next.
- **English and Spanish** in the same question record — switch language at any
  time, mid-exam included.

## Requirements

**Python 3.10 or newer.** That's it.

You do *not* need to install Node, and you do *not* need to install a database
engine. Reflex downloads its own JavaScript runtime on first run, and the app
stores your history in SQLite, which ships inside Python's standard library.

## Getting started

```bash
git clone git@github.com:slackwero/google-GCP-associate-cloud-engineer-exam-prep.git
cd google-GCP-associate-cloud-engineer-exam-prep/quiz-app

python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

.venv/bin/reflex run
```

Then open <http://localhost:3000>.

Two things worth knowing:

- **The first run takes a while** (a minute or more). Reflex is downloading its
  JavaScript runtime and compiling the frontend. Later runs start quickly.
- **Internet is only needed to install.** Once set up, the app works offline:
  the question bank and the fonts are both in the repository.

The database is created automatically on first run. You start with an empty
history and the full question bank.

If ports 3000/8000 are still busy from a previous session:

```bash
lsof -ti:3000,8000 | xargs kill -9
```

## How your data is stored

| | Where | Tracked in git? |
|---|---|---|
| **Question bank, courses, services, blueprint** | JSON files in `quiz-app/data/` | Yes |
| **Your attempts and answers** | SQLite at `quiz-app/quiz_ace.db` | **No** |

Content is versioned like code: it is reviewed in diffs and validated by the
test suite. Your progress is yours and never leaves your machine — deleting
`quiz_ace.db` resets your history and nothing else.

## Development

```bash
cd quiz-app
.venv/bin/pip install -r requirements-dev.txt

.venv/bin/pytest          # 57 tests, including the blueprint coverage gate
.venv/bin/ruff check .    # lint
```

The test suite validates the question bank itself: schema, bilingual fields,
blueprint mapping, and minimum coverage per sub-topic and per course. An invalid
question is excluded with a warning rather than breaking the app.

## Project layout

```
quiz-app/
  data/                 question bank + catalogs (JSON, bilingual)
  quiz_ace/
    services/           pure Python logic, no Reflex — this is what the tests cover
    states/             Reflex state (language, quiz, exam, progress)
    components/         UI primitives and shared pieces
    pages/              the 7 routes
  assets/theme.css      the design system: every colour, shape and motion token
recursos/               official exam guides, coverage analysis, study plan
```

## License

**Not yet decided.** Until a license file is added, default copyright applies and
no reuse rights are granted.

The bundled Roboto font files are a separate matter: they are distributed under
the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), as
documented in
[`quiz-app/assets/fonts/README.md`](quiz-app/assets/fonts/README.md).
