import streamlit as st
import transformers
from src.summarizer import summarize_to_soap

st.set_page_config(page_title="Salamancas Notes", page_icon="📝", layout="centered")
st.title("📝 Salamancas Notes")
st.caption("Local Hugging Face models only • Summarize EHR text → SOAP note")

mode = st.radio("Choose model", ["FLAN‑T5 (instruction)", "BART (summarization)"], index=0)

uploaded = st.file_uploader("Optional: Upload a .txt file", type=["txt"])
text = ""
if uploaded:
    text = uploaded.read().decode("utf-8", errors="ignore")
text = st.text_area("Clinical / EHR text", value=text, height=280, placeholder="Paste long clinical text here...")

if st.button("Generate SOAP Note", type="primary", disabled=not text.strip()):
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
else:
    st.info("Paste text or upload a .txt file, then click Generate.")
