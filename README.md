# 🧠 Salamanca Notes  
### *Because doctors deserve fewer words and more sense.*

![Made with ❤️ at UNT](https://img.shields.io/badge/Made%20with%20%E2%9D%A4%EF%B8%8F%20at-UNT-green?style=for-the-badge)
![Built with Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red?style=for-the-badge)
![HackWell 2025](https://img.shields.io/badge/HackWell%202025-Health%20Informatics-blue?style=for-the-badge)

---

## 🚀 What is this?

**Salamanca Notes** is your local AI sidekick for summarizing long, messy **Electronic Health Records (EHRs)** into clean, structured **SOAP notes** — *without ever sending data to the cloud*.  

Built for hackathons, hospitals, and heroic students pulling all-nighters.  
It runs offline, keeps patient info private, and produces professional-grade summaries in seconds.  

🩺 **S**ubjective  
🧾 **O**bjective  
💬 **A**ssessment  
📋 **P**lan  

That’s it. Four sections. One calm, concise summary.  

---

## 🧩 How it works

It runs **locally** using open-source models from Hugging Face:  

| Model | Role | Personality |
|--------|------|-------------|
| 🧠 `google/flan-t5-base` | Instruction-following model | “Yes doc, here’s your structured SOAP note.” |
| 💊 `facebook/bart-large-cnn` | Summarizer | “Fast, neat, and occasionally improvises.” |

No API keys, no OpenAI bills, no cloud dependencies.  
Your data stays on your machine — the way HIPAA intended.  

---

## ⚙️ Setup (Windows)

```powershell
# 1️⃣ Open PowerShell in your project folder
cd "C:\Projects\SalamancaNotes"

# 2️⃣ Create & activate a virtual environment
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

# 3️⃣ Install dependencies
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 4️⃣ Launch the app
streamlit run app.py
