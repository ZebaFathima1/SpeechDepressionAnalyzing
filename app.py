import streamlit as st
import whisper
import google.generativeai as genai

# ===============================
# GEMINI API KEY
# ===============================
genai.configure(api_key="AIzaSyAQdhOuvXPOO_dCnGgXJdlOT-M3Zz4G9mA")
gemini = genai.GenerativeModel("gemini-1.5-flash")

# ===============================
# LOAD WHISPER MODEL
# ===============================
@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

whisper_model = load_whisper()

# ===============================
# UI
# ===============================
st.set_page_config(page_title="AI Speech Well-being Assistant", layout="centered")
st.title("🎧 AI Speech-Based Well-being Assistant")
st.write("Upload a short WAV audio file (10–30 seconds).")

uploaded = st.file_uploader("Upload WAV file", type=["wav"])

if uploaded:
    st.audio(uploaded)

    with st.spinner("Transcribing speech..."):
        result = whisper_model.transcribe(uploaded)
        transcript = result["text"]

    st.subheader("📝 Transcription")
    st.write(transcript)

    with st.spinner("Analyzing with Gemini..."):
        response = gemini.generate_content(
            f"""
            You are a mental well-being assistant.

            Based on the following transcript, analyze:
            1. Emotional tone
            2. Stress or low-mood indicators
            3. Overall well-being risk (low / moderate / high)

            DO NOT diagnose depression.
            Provide supportive, non-clinical feedback.

            Transcript:
            {transcript}
            """
        )

    st.subheader("🧠 AI Analysis")
    st.write(response.text)

st.markdown("""
⚠️ **Disclaimer**  
This tool provides general well-being insights only  
and does not diagnose mental health conditions.
""")
