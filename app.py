import streamlit as st
import soundfile as sf
import tempfile
import warnings
from audiorecorder import audiorecorder
import google.generativeai as genai

warnings.filterwarnings("ignore")

# ===============================
# GEMINI API KEY (EASY WAY)
# ===============================
genai.configure(api_key="AIzaSyAQdhOuvXPOO_dCnGgXJdlOT-M3Zz4G9mA")

model = genai.GenerativeModel("gemini-1.5-pro")

# ===============================
# STREAMLIT UI
# ===============================
st.set_page_config(
    page_title="AI Speech Well-being Assistant",
    layout="centered"
)

st.title("🎤 AI Speech-Based Well-being Assistant")
st.write("Click **Start Recording**, speak for 10–30 seconds, then stop.")

# ===============================
# MICROPHONE INPUT
# ===============================
audio = audiorecorder("🎙 Start Recording", "⏹ Stop Recording")

if len(audio) > 0:
    st.audio(audio.export().read(), format="audio/wav")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        sf.write(tmp.name, audio.to_numpy_array(), audio.sample_rate)

        with open(tmp.name, "rb") as f:
            audio_bytes = f.read()

    with st.spinner("Analyzing speech with Gemini AI..."):
        response = model.generate_content(
            [
                {
                    "mime_type": "audio/wav",
                    "data": audio_bytes
                },
                """
                You are a mental well-being assistant.

                Analyze the speech for:
                1. Emotional tone
                2. Stress or low-mood indicators
                3. Overall well-being risk (low / moderate / high)

                DO NOT diagnose depression.
                Provide supportive, non-clinical feedback.
                """
            ]
        )

    st.subheader("🧠 AI Analysis")
    st.write(response.text)

# ===============================
# DISCLAIMER
# ===============================
st.markdown("""
⚠️ **Disclaimer**  
This tool provides **general well-being insights only**  
and is **not a medical or diagnostic system**.
""")
