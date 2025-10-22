import streamlit as st
from src.summarizer import summarize_to_soap
from src.speech_to_text import transcribe_audio_to_english

st.set_page_config(page_title="Salamanca Notes", page_icon="🧠", layout="centered")
st.title("🧠 Salamanca Notes")
st.caption("Local EHR Summarizer — now with Spanish speech → English transcript → SOAP note")

tab_text, tab_audio = st.tabs(["📝 Text → SOAP", "🎙️ Spanish Audio → SOAP"])

# ───────────────────────────
# Tab 1: Text → SOAP
# ───────────────────────────
with tab_text:
    st.subheader("Paste EHR text or upload a .txt file")
    mode = st.radio("Choose model", ["FLAN-T5 (instruction)", "BART (summarization)"], index=0, horizontal=True)

    uploaded = st.file_uploader("Optional: Upload a .txt", type=["txt"], key="txt_upload")
    text = ""
    if uploaded:
        text = uploaded.read().decode("utf-8", errors="ignore")

    text = st.text_area("Clinical / EHR text", value=text, height=260, placeholder="Paste clinical text here...")

    if st.button("Generate SOAP Note", type="primary", disabled=not text.strip(), key="txt_btn"):
        with st.spinner("Generating..."):
            mode_key = "flan" if mode.startswith("FLAN") else "bart"
            soap = summarize_to_soap(text.strip(), mode=mode_key)

        st.subheader("SOAP Clinical Note")
        st.markdown(f"**Subjective:** {soap['Subjective']}")
        st.markdown(f"**Objective:** {soap['Objective']}")
        st.markdown(f"**Assessment:** {soap['Assessment']}")
        st.markdown(f"**Plan:** {soap['Plan']}")

        full_txt = (
            "Subjective: " + soap["Subjective"] + "\n\n"
            "Objective: " + soap["Objective"] + "\n\n"
            "Assessment: " + soap["Assessment"] + "\n\n"
            "Plan: " + soap["Plan"] + "\n"
        )
        st.download_button("Download summary (.txt)", full_txt, file_name="soap_summary.txt")

# ───────────────────────────
# Tab 2: Spanish Audio → SOAP
# ───────────────────────────
with tab_audio:
    st.subheader("Upload Spanish audio (WAV / MP3 / M4A)")
    mode_a = st.radio("Choose model", ["FLAN-T5 (instruction)", "BART (summarization)"], index=0, horizontal=True, key="a_model")

    audio = st.file_uploader("Audio file", type=["wav", "mp3", "m4a"], key="audio_upload")
    transcript = ""

    if audio:
        tmp_path = f"./tmp_{audio.name}"
        with open(tmp_path, "wb") as f:
            f.write(audio.read())
        st.audio(tmp_path)

        with st.spinner("Transcribing (Spanish → English)…"):
            transcript = transcribe_audio_to_english(tmp_path, source_lang="es")

        st.text_area("English Transcript (auto-generated)", value=transcript, height=180)

        if st.button("Generate SOAP Note from Transcript", type="primary", key="audio_btn"):
            with st.spinner("Summarizing..."):
                mode_key = "flan" if mode_a.startswith("FLAN") else "bart"
                soap = summarize_to_soap(transcript.strip(), mode=mode_key)

            st.subheader("SOAP Clinical Note")
            st.markdown(f"**Subjective:** {soap['Subjective']}")
            st.markdown(f"**Objective:** {soap['Objective']}")
            st.markdown(f"**Assessment:** {soap['Assessment']}")
            st.markdown(f"**Plan:** {soap['Plan']}")

            full_txt = (
                "Subjective: " + soap["Subjective"] + "\n\n"
                "Objective: " + soap["Objective"] + "\n\n"
                "Assessment: " + soap["Assessment"] + "\n\n"
                "Plan: " + soap["Plan"] + "\n"
            )
            st.download_button("Download summary (.txt)", full_txt, file_name="soap_summary_from_audio.txt")
    else:
        st.info("Upload a Spanish audio file to continue.")

