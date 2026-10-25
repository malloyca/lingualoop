# LinguaLoop

LinguaLoop is a local-first language-learning workspace for deliberate,
model-assisted practice. It is designed as a personal harness for rebuilding
and maintaining language ability—not as a structured-course or Duolingo
replacement.

The learner keeps independent profiles for languages such as Japanese and
Taiwanese Mandarin, manually records vocabulary and grammar they want to
practise, and chats with a tutor through a user-configured LLM endpoint. The
app uses that profile data to make conversation more relevant now and to
support practice activities later.

## Current direction

The project is in its design/foundation stage.

The guiding idea is:

```text
Learner profile + manually maintained targets + conversation history
                              ↓
                    profile-aware tutor chat
                              ↓
          future learner-selected practice activities
```

## v0.1 — local learner workspace

**Goal:** A useful, persistent local browser application for maintaining
learner data and having profile-aware text conversations.

The learner can:

- create, edit, select, and archive independent language profiles;
- manually create, edit, search, and archive vocabulary and grammar targets;
- configure and test one app-wide OpenAI-compatible text-chat endpoint;
- start, resume, and browse conversations for a selected profile; and
- explicitly request a correction review that follows that profile's
  correction preference.

v0.1 deliberately does **not** include generated daily sessions, flashcards,
spaced repetition, automatic mistake/target extraction, voice, image-based
practice, accounts, cloud sync, or a bundled model.

### Initial architecture

```text
Browser (HTML, CSS, JavaScript)
             │
             ▼
FastAPI API
             │
             ▼
Application / learning-domain services
  ├── profiles and targets
  ├── conversations and correction reviews
  ├── tutor-context construction
  └── provider configuration
       │                 │
       ▼                 ▼
SQLite repositories   OpenAI-compatible LLM provider
```

This separation keeps learner logic independent of the browser, FastAPI, and
the selected model runner. LM Studio is an expected initial local endpoint, but
the app is not coupled to it. A future managed endpoint or packaged local model
can implement the same provider boundary.

### Technology choices

- Python and `uv`
- FastAPI
- SQLite with versioned migrations
- HTML, CSS, and modern JavaScript
- An OpenAI-compatible text-chat API, initially suitable for LM Studio

The first frontend should remain plain and local: a chat workspace plus
Profiles, Vocabulary, Grammar, and Settings views. A JavaScript framework is
not a v0.1 requirement.

## Development workflow

The FastAPI application is defined in `src/lingualoop/main.py`. A chat request
is validated by the API schema, turned into a system prompt and learner message
in `conversations.py`, sent to the OpenAI-compatible endpoint by `llm.py`, and
returned as a response. The endpoint (`http://localhost:1234/v1`) and model
(`qwen/qwen3.8-27b`) in `main.py` are temporary proof-of-concept values; T06
will replace them with editable provider settings.

Install the locked project dependencies and run the local server with:

```sh
uv sync
uv run uvicorn lingualoop.main:app --reload
```

Run the offline automated tests with:

```sh
uv run pytest
```

The baseline API test uses a fake model client, so it does not need LM Studio or
any other LLM endpoint. The separate `test_llm.py` script is an opt-in
integration smoke test; run it explicitly only when the configured local model
server is available:

```sh
uv run python test_llm.py
```

## Roadmap

### v0.2 — learner-selected practice activities

Generate a menu of options such as simple target review, guided questions,
free conversation, and role-play scenarios. Role-play plans will specify the
situation, learner role, tutor persona, communication goal, and relevant
targets; the learner chooses an activity rather than receiving a fixed lesson.

### v0.3 — learning signals

Add learner-approved suggestions for vocabulary and grammar targets, record
activity history and recurring mistakes, and use that information to make
recommendations more useful.

### v0.4+ — adaptive multimodal practice

Add spaced-repetition scheduling, voice, picture/vision activities where the
configured model supports them, progress views, and model/prompt evaluation.

## Design principles

- Keep the app local-first and the learner in control of their data.
- Keep the LLM backend replaceable.
- Make language-learning logic independent of FastAPI and frontend code.
- Build working vertical slices instead of premature abstractions.
- Treat LLM output as fallible; do not silently turn it into learner records.
- Let actual daily use shape the learning system.
