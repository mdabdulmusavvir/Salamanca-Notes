from typing import Dict, Literal
from transformers import pipeline

# ──────────────────────────────────────────────────────────────────────────────
# Models:
#  - FLAN-T5 (instruction-following) → best for explicit SOAP structure
#  - BART (summarization)            → strong summarizer; we post-split into SOAP
# ──────────────────────────────────────────────────────────────────────────────
_inst = pipeline("text2text-generation", model="google/flan-t5-base")          # ~250M, CPU-friendly
_summ = pipeline("summarization", model="facebook/bart-large-cnn")             # summarizer fallback

SOAP_SYSTEM_INSTRUCTION = (
    "You are a clinical scribe. Produce a concise SOAP note with the EXACT four "
    "headings and a single paragraph per heading:\n"
    "Subjective:\nObjective:\nAssessment:\nPlan:\n\n"
    "Rules:\n"
    "- Professional, neutral tone.\n"
    "- 150–220 words total across all sections.\n"
    "- If a section lacks information, write: \"Not mentioned\".\n"
)

def _flan_prompt(clinical_text: str) -> str:
    """
    Build a prompt that clearly separates instruction from input so the model
    doesn't treat instructions as patient text.
    """
    return (
        f"Instruction:\n{SOAP_SYSTEM_INSTRUCTION}\n"
        f"Clinical Text:\n{clinical_text}\n\n"
        f"Now generate only the SOAP note with these four headings."
    )

def _bart_prompt(clinical_text: str) -> str:
    # BART is a summarizer; prepend a light instruction to bias the output
    return (
        f"{SOAP_SYSTEM_INSTRUCTION}\n"
        f"Clinical Text:\n{clinical_text}\n"
        f"Summarize into a SOAP note."
    )

def _force_soap_sections(text: str) -> Dict[str, str]:
    """
    Heuristically split model output into SOAP sections.
    If headings are missing, put everything under Subjective and mark others.
    """
    sections = {
        "Subjective": "Not mentioned",
        "Objective": "Not mentioned",
        "Assessment": "Not mentioned",
        "Plan": "Not mentioned",
    }

    # Normalize line breaks and collapse excessive whitespace
    t = " ".join(text.replace("\r", "\n").split())

    # Strong parse using explicit tags
    tags = ["Subjective:", "Objective:", "Assessment:", "Plan:"]
    found = False
    for i, tag in enumerate(tags):
        if tag in t:
            found = True
            after = t.split(tag, 1)[1]
            # until next tag or end
            tail = after
            for nxt in tags[i+1:]:
                if nxt in after:
                    tail = after.split(nxt, 1)[0]
                    break
            content = tail.strip()
            if content:
                # Limit runaway generations a bit
                sections[tag[:-1]] = content[:1200].strip()

    if not found:
        # Model ignored headings; fall back to putting all in Subjective
        sections["Subjective"] = text.strip()

    # Final cleanup: avoid echoing our instruction if model copied it
    for k, v in sections.items():
        if "You are a clinical scribe" in v or "Instruction:" in v:
            sections[k] = "Not mentioned"

    return sections

def summarize_to_soap(
    clinical_text: str,
    mode: Literal["flan", "bart"] = "flan",
) -> Dict[str, str]:
    """
    Summarize free-form clinical/EHR text into SOAP sections using local models only.
    - mode='flan' uses google/flan-t5-base (instruction-following)
    - mode='bart' uses facebook/bart-large-cnn (summarization)
    """
    clinical_text = clinical_text.strip()
    if not clinical_text:
        return {
            "Subjective": "Not mentioned",
            "Objective": "Not mentioned",
            "Assessment": "Not mentioned",
            "Plan": "Not mentioned",
        }

    if mode == "flan":
        prompt = _flan_prompt(clinical_text)
        out = _inst(prompt, max_new_tokens=256, do_sample=False)[0]["generated_text"]
    else:
        prompt = _bart_prompt(clinical_text)
        # Shorten very long inputs for BART to avoid truncation crashes
        max_chars = 5000
        if len(prompt) > max_chars:
            prompt = prompt[:max_chars]
        out = _summ(prompt, max_length=240, min_length=120, do_sample=False)[0]["summary_text"]

    return _force_soap_sections(out.strip())
