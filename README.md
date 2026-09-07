# LinguaLoop

A local, voice-oriented language-learning chatbot for natural daily conversation practice.

## Roadmap

### v0.1 — Text Conversation

**Goal:** A functional local web chatbot that feels like a language-learning conversation partner.

* [ ] **Project skeleton**

  * Python project managed with `uv`
  * FastAPI application
  * Basic `/health` endpoint

* [ ] **LLM client**

  * Connect to LM Studio's OpenAI-compatible API
  * Abstract LLM communication behind an `LLMClient`
  * Verify local model communication

* [ ] **FastAPI backend**

  * `/api/chat` endpoint
  * Pydantic request/response models
  * Keep application logic separate from web/API code

* [ ] **Web UI**

  * Simple HTML/CSS/JavaScript chat interface
  * Send and display messages

* [ ] **Streaming**

  * Stream LLM responses from LM Studio → FastAPI → browser
  * Investigate Server-Sent Events (SSE)

* [ ] **Persistence**

  * SQLite database
  * Store conversations and messages
  * Resume conversations after restarting the browser/app

* [ ] **Language-learning behavior**

  * Configurable language/locale
  * Traditional Chinese / Taiwanese Mandarin as initial configuration
  * Learner proficiency and correction-level settings
  * Language-learning system prompt

* [ ] **Correction mode**

  * Analyze recent learner messages on request
  * Return useful grammar/vocabulary/naturalness corrections
  * Use structured LLM output where appropriate

**v0.1 milestone:** Have a natural text conversation with the local LLM and optionally ask it to analyze/correct mistakes.

---

### v0.2 — Voice Conversation

**Goal:** Make voice interaction a first-class part of the language-learning experience.

#### STT

* [ ] Capture microphone audio in browser
* [ ] Send audio to backend
* [ ] Integrate local/appropriate speech-to-text system
* [ ] Feed transcription into the existing chat pipeline

#### TTS

* [ ] Integrate text-to-speech
* [ ] Convert LLM responses to audio
* [ ] Stream/play audio in browser

#### Integration

* [ ] Combine STT → LLM → TTS into a natural conversational loop
* [ ] Display transcription alongside audio
* [ ] Handle recording, processing, and playback states

**v0.2 milestone:** Have a spoken conversation with the local language tutor.

---

### v0.3 — Learning System

* [ ] Vocabulary tracking
* [ ] Recurring mistake tracking
* [ ] Learner profile
* [ ] Conversation/topic history
* [ ] Deliberate vocabulary practice

### v0.4+ — Advanced Learning Features

* [ ] Spaced repetition
* [ ] Progress tracking
* [ ] Model/prompt evaluation
* [ ] More sophisticated personalization
* [ ] Additional languages
* [ ] Other features driven by actual usage

## Design Principles

* Keep the application **local-first**.
* Keep the LLM backend replaceable.
* Keep language-learning logic independent of FastAPI.
* Prefer simple architecture over premature abstraction.
* Build each feature as a working vertical slice.
* Don't build advanced learning features until the basic conversation experience is genuinely useful.
* Let actual daily use determine future features.

## Initial Architecture

```text
Browser
   │
   ▼
FastAPI
   │
   ├── Conversation / Learning Logic
   ├── SQLite
   │
   └── LLMClient
          │
          ▼
      LM Studio
          │
          ▼
       Local LLM
```

### v0.2 Extension

```text
Microphone
    │
    ▼
 Browser ──► FastAPI ──► STT
                         │
                         ▼
                   Conversation
                         │
                         ▼
                        LLM
                         │
                         ▼
                        TTS
                         │
                         ▼
 Browser ◄──────────── Audio
```

## Initial Technology Stack

* **Python**
* **uv**
* **FastAPI**
* **SQLite**
* **HTML / CSS / JavaScript**
* **LM Studio**
* Local LLM (initially Qwen or another suitable model)
