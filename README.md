# 🧠 Salamanca Notes  
### Because doctors deserve fewer words and more sense.

---

## 1️⃣ Context
Doctors spend a crazy amount of time typing up patient notes — sometimes more than they spend with actual patients.  
In Texas and many other regions, a large Hispanic population also means there’s a **language gap** between Spanish-speaking patients and English-speaking doctors.  

That’s a lot of chaos in communication.  
So… we decided to fix it.  

Enter **Salamanca Notes** — your friendly neighborhood AI scribe.

---

## 2️⃣ Vision
Imagine this:  
A doctor talks. The AI listens — in Spanish or English.  
And *boom*, it creates a clean, professional **SOAP note** (Subjective, Objective, Assessment, Plan).  

No endless typing.  
No “wait, what did they say?”  
Just quick, clean summaries, all done **locally** — no cloud, no patient data leaks.

Our goal?  
Make healthcare documentation effortless, accurate, and inclusive.

---

## 3️⃣ What We’ve Done So Far
✅ Built a Streamlit app that converts raw EHR text into structured SOAP notes.  
✅ Integrated local summarization models (**FLAN-T5** and **BART**) — both open-source.  
✅ Added **Whisper (speech-to-text)** for Spanish audio input.  
✅ Added **Helsinki-NLP translation** for Spanish → English conversion.  
✅ Kept everything **offline** for privacy.  
✅ Tested it on sample audio and mock medical records.  

Basically, we made AI the intern who never complains.

---

## 4️⃣ How It Works (In Simple Words)
🎙️ Speak in Spanish or upload an audio file.  
🧠 Whisper converts speech → Spanish text.  
🌐 Translator converts Spanish → English.  
📋 Summarizer builds a neat SOAP note.  
💾 Everything stays on your laptop — zero cloud dependency.  

You talk → it listens → you get a professional clinical note before your coffee gets cold.

---

## 5️⃣ Future Impact
When we ship this to production, **Salamanca Notes** could:
- ⚡ Save doctors hours of typing every week  
- 🗣️ Break language barriers between patients and doctors  
- 🔒 Protect patient privacy (offline, local models)  
- 🌎 Support multilingual healthcare — not just Spanish  

It’s not just a hackathon project. It’s a step toward **human-centered AI for healthcare**.

---

## 6️⃣ Tech Stack
| Layer | Tool | Why |
|-------|------|-----|
| 🎨 UI | Streamlit | Simple and fast for prototyping |
| 🧠 NLP | Hugging Face Transformers | Open-source power |
| 🗣️ Speech-to-Text | Faster-Whisper | Accurate and local |
| 🌐 Translation | Helsinki-NLP (es→en) | Lightweight and offline |
| ⚙️ Backend | Python 3.11 | Because of course |
| 🧾 Summary Models | FLAN-T5 / BART | Great for structured outputs |

---

## 7️⃣ How to Run
```bash
# Create and activate your venv
python -m venv .venv
.\.venv\Scripts\activate  # (Windows)
# or source .venv/bin/activate  # (Mac/Linux)

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
