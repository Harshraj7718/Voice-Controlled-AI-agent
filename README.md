# 🎙 Voice-Controlled Local AI Agent

> A fully offline, end-to-end AI pipeline that turns spoken commands into real actions —  
> speech recognition via Hugging Face Whisper, reasoning via Ollama LLaMA 3, and a  
> polished dark-mode Streamlit interface.

---

## 📌 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Project Structure](#project-structure)
5. [Prerequisites](#prerequisites)
6. [Installation & Setup](#installation--setup)
7. [Running the App](#running-the-app)
8. [Usage Guide](#usage-guide)
9. [Hardware Workarounds](#hardware-workarounds)
10. [Troubleshooting](#troubleshooting)
11. [Model Reference](#model-reference)
12. [Submission Links](#submission-links)
13. [Author](#author)

---

## Overview

This project is a **Voice-Controlled Local AI Agent** that accepts audio input (uploaded file or live microphone), transcribes it using Whisper, infers the user's intent using a local LLM, and executes the appropriate action — all without any external API calls.

It demonstrates a complete **Generative AI + System Design** pipeline suitable for real-world offline deployment.

---

## Features

| Category | Details |
|---|---|
| 🎤 **Audio Input** | Upload `.wav` / `.mp3`, or record 5 seconds live from microphone |
| 🔊 **Speech-to-Text** | Hugging Face Whisper `openai/whisper-base`, fully local inference |
| 🧠 **Intent Detection** | Ollama LLaMA 3 extracts structured JSON intent from transcribed text |
| ⚙️ **Tool Execution** | `create_file`, `write_code`, `summarize`, `chat_response` |
| 🔄 **Multi-intent** | Handles compound voice commands in a single utterance |
| ✏️ **Human-in-the-loop** | Editable transcription before any action is triggered |
| 🧠 **Session Memory** | Full history tracked across the session |
| 🎨 **Styled UI** | Custom dark-mode Streamlit interface with external CSS |
| ❌ **Error Handling** | Graceful fallback at every stage of the pipeline |

---

## Architecture

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│                  (Streamlit — app.py + style.css)               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    Audio Input Layer
               ┌─────────────┴─────────────┐
               │                           │
        File Upload                  Microphone
        (.wav / .mp3)              (5-sec live record)
               │                           │
               └─────────────┬─────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SPEECH-TO-TEXT  (stt.py)                       │
│          Hugging Face Whisper — openai/whisper-base             │
│          Runs locally on CPU · FP32 · No internet needed        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                   Transcribed text string
                             │
                    ┌────────▼────────┐
                    │  User can EDIT  │  ← Human-in-the-loop
                    │  transcription  │
                    └────────┬────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 INTENT DETECTION  (intent.py)                   │
│              Ollama LLaMA 3 — local inference                   │
│      Returns structured JSON: { intent, filename, ... }        │
│      Supports multi-intent: list of action objects             │
└────────────────────────────┬────────────────────────────────────┘
                             │
               User confirms before execution
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  TOOL EXECUTION  (tools.py)                     │
│                                                                 │
│   create_file ──── Creates an empty file in output/            │
│   write_code  ──── Generates + saves AI-written Python code     │
│   summarize   ──── Summarises text via LLM                     │
│   chat        ──── General conversational response             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SESSION MEMORY  (memory.py)                    │
│     Saves { text, intent, filename, result } per action        │
│     Displayed in reverse-chronological order on History page   │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| File | Role |
|---|---|
| `app.py` | Streamlit UI, page routing, pipeline orchestration |
| `style.css` | All visual styles — loaded at runtime via `open(..., encoding="utf-8")` |
| `stt.py` | Loads Whisper model, accepts audio path, returns transcript string |
| `intent.py` | Prompts LLaMA 3 via Ollama, parses JSON intent from response |
| `tools.py` | Executes actions; writes files safely inside `output/` directory |
| `mic.py` | Records 5 seconds of audio from default microphone, saves to `.wav` |
| `memory.py` | In-memory list of session history; `save()` and `get()` helpers |

---

## Project Structure

```
voice-ai-agent/
│
├── app.py              # Main Streamlit application
├── style.css           # External dark-mode UI styles
│
├── stt.py              # Speech-to-Text (Whisper)
├── intent.py           # Intent detection (Ollama LLaMA 3)
├── tools.py            # Tool execution logic
├── mic.py              # Microphone recording
├── memory.py           # Session memory
│
├── output/             # All generated files written here (safe sandbox)
│
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## Prerequisites

Before installing Python packages, make sure the following are in place:

### 1. Python 3.9 – 3.11

> ⚠️ Python 3.12+ may have compatibility issues with some PyTorch builds. Python 3.10 is recommended.

```bash
python --version
```

### 2. FFmpeg

Required by Whisper to decode `.mp3` and other audio formats.

**Windows:**
1. Download a build from [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract the archive
3. Add the `bin\` folder to your system `PATH`
4. Verify installation: `ffmpeg -version`

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Linux (apt):**
```bash
sudo apt install ffmpeg
```

### 3. Ollama + LLaMA 3

1. Download and install Ollama from [ollama.com](https://ollama.com)
2. Pull and start LLaMA 3:

```bash
ollama run llama3
```

> Ollama must be running in the background before launching the app.  
> Default endpoint used by this project: `http://localhost:11434`

---

## Installation & Setup

### Step 1 — Clone the repository

```bash
git clone <your-repo-link>
cd voice-ai-agent
```

### Step 2 — Create a virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

> The first run will automatically download the Whisper model (~500 MB) from Hugging Face.  
> An internet connection is only required for this one-time download.

### Step 4 — Start Ollama in a separate terminal

```bash
ollama run llama3
```

Leave this terminal open. The app communicates with Ollama over localhost on every request.

---

## Running the App

```bash
python -m streamlit run app.py
```

Open your browser to `http://localhost:8501` if it does not open automatically.

---

## Usage Guide

### Dashboard

1. **Upload** a `.wav` or `.mp3` file, or click **Record (5 sec)** to capture live audio.
2. The transcribed text appears in an **editable text box** — correct any recognition errors before proceeding.
3. Toggle **"Use edited version"** to choose which text is sent to the LLM.
4. Review the **detected intent** displayed as JSON, then click **Confirm & Execute** to run the action.
5. Results appear as styled cards beneath the button.

### History Page

All processed commands are logged here in reverse chronological order, showing the original input, detected intent badge, and execution result.

### Example Commands

```
"Create a Python file with a retry function."
"Write Python code for factorial and save it."
"Summarize this text."
"Hello, how are you?"
"Create a file and write code in it."      ← multi-intent example
```

---

## Hardware Workarounds

This project is designed to run on **standard consumer hardware without a GPU**. The following workarounds were applied to make that practical.

---

### 1. CPU-only Whisper inference (FP32 mode)

By default, Hugging Face Transformers will attempt to use a CUDA GPU if available. Since most development machines lack a suitable GPU, Whisper is loaded without specifying a device, forcing a CPU fallback:



**Why `whisper-base`?**  
It is the smallest Whisper variant that still produces usable accuracy (~74M parameters, ~500 MB download). Larger variants (`small`, `medium`, `large`) are more accurate but 3–10× slower on CPU and may cause out-of-memory errors on machines with less than 8 GB RAM.

**Trade-off:** Transcribing a 5-second clip takes roughly 5–20 seconds on a modern CPU. This is acceptable for a voice assistant with a confirmation step.

---

### 2. Local LLM via Ollama (4-bit quantisation, no VRAM required)

Loading LLaMA 3 directly into Python (e.g. via `transformers`) would require 16+ GB of VRAM in full precision. Instead, Ollama runs LLaMA 3 as a background server with **4-bit quantisation**, reducing memory usage to roughly 4–5 GB of RAM.

The app communicates with it over a local HTTP endpoint:



**Benefits:**
- No API keys or token costs
- Works fully offline after the initial `ollama pull`
- Ollama manages memory automatically — no manual batching needed

**Trade-off:** LLM responses take 5–30 seconds on CPU depending on output length. Keeping prompts short and instructing the model to return only JSON significantly reduces latency.

---

### 3. Microphone recording at 16 kHz (Whisper's native sample rate)

`sounddevice` wraps PortAudio and works without PulseAudio, ASIO, or any heavyweight audio server — making it cross-platform with no driver configuration.

Recording is done directly at **16,000 Hz**, which is Whisper's native sample rate:

```python
# mic.py
import sounddevice as sd
import scipy.io.wavfile as wav

SAMPLE_RATE = 16000  # Whisper's native rate — no resampling needed
DURATION    = 5      # seconds

recording = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1
)
sd.wait()
wav.write("temp.wav", SAMPLE_RATE, recording)
```

Recording at the correct sample rate avoids a resampling step, which reduces both processing time and any quality loss from format conversion.

---

### 4. UTF-8 CSS loading (Windows `cp1252` compatibility fix)

Windows defaults to the `cp1252` codec when opening text files. `style.css` contains box-drawing characters (e.g. `──`) used in comments, which `cp1252` cannot decode — causing a `UnicodeDecodeError` on startup.

Fix applied in `app.py`:

```python
def load_css(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:   # explicit UTF-8
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
```

This makes the app behave identically on Windows, macOS, and Linux.

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `UnicodeDecodeError` on startup | Windows reads CSS as `cp1252` | Ensure `encoding="utf-8"` is in `load_css()` |
| `ffmpeg not found` error | FFmpeg not in system PATH | Re-install FFmpeg and restart terminal |
| Whisper download hangs | Slow connection or Hugging Face rate limit | Retry — model is cached after first successful download |
| `Connection refused` from Ollama | Ollama server not running | Run `ollama run llama3` in a separate terminal |
| Microphone not detected | Wrong default audio device | Check OS sound settings; try a USB microphone |
| Very slow transcription | CPU-only inference | Expected behaviour — use clips under 10 seconds |
| JSON parse error from LLM | LLaMA 3 returned prose instead of JSON | Retry the request; tighten the JSON instruction in `intent.py` |
| `torch` install fails | Python version mismatch | Use Python 3.10; install PyTorch manually from [pytorch.org](https://pytorch.org) |

---

## Model Reference

| Component | Model | Quantisation | Runtime |
|---|---|---|---|
| Speech-to-Text | `openai/whisper-base` (Hugging Face) | FP32 (full) | Local CPU |
| Intent Detection | LLaMA 3 8B (Ollama) | 4-bit (Q4_0) | Local CPU |
| Code Generation | LLaMA 3 8B (Ollama) | 4-bit (Q4_0) | Local CPU |
| Summarization | LLaMA 3 8B (Ollama) | 4-bit (Q4_0) | Local CPU |

---

## Submission Links

| | |
|---|---|
| 📂 GitHub Repository | https://github.com/Harshraj7718/Voice-Controlled-AI-agent |
| 🎥 Demo Video | https://youtu.be/d3inBfQQVqk |
| ✍️ Article | https://medium.com/@rajharsh71018/voice-controlled-ai-agent-with-local-llms-whisper-ollama-5e730b946f25 |

---

## Author

**Harsh Raj**  
AI/ML & Generative AI Developer

