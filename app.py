import streamlit as st
import google.generativeai as genai
import warnings

warnings.filterwarnings("ignore")

# ===============================
# GEMINI API KEY (EASY WAY)
# ===============================
genai.configure(api_key="PASTE_YOUR_GEMINI_API_KEY_HERE")

model = genai.GenerativeModel("gemini-1.5-pro")

# ===============================
# STREAMLIT UI
# ===============================
st.set_page_config(page_title="AI Speech Well-being Assistant", layout="centered")

st.title("🎧 AI Speech-Based Well-being Assistant")
st.write("Upload a short WAV audio file (10–30 seconds).")

uploaded_file = st.file_uploader("Upload WAV file", type=["wav"])

if uploaded_file:
    st.audio(uploaded_file, format="audio/wav")

    audio_bytes = uploaded_file.read()

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

st.markdown("""
⚠️ **Disclaimer**  
This tool provides **general well-being insights only**  
and is **not a medical or diagnostic system**.
""")
