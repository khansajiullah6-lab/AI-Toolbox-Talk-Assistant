import streamlit as st
from google import genai

# Page Setup
st.set_page_config(page_title="AI Toolbox Talk Assistant", layout="wide", page_icon="📢")

st.title("📢 AI Toolbox Talk (TBT) Assistant")
st.markdown("Aap jo bhi safety topic yahan likhenge, AI uske upar workers ko samjhane ke liye **TBT Points** taiyaar kar dega.")

# Sidebar for API Key
st.sidebar.markdown("## 🔑 AI Configuration")
api_key = st.sidebar.text_input("Apni Google Gemini API Key yahan dalein:", type="password")

if not api_key:
    st.warning("⚠️ App chalane ke liye kripya left sidebar mein apni Gemini API Key dalein.")
else:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Initialization Error: {e}")

    # User Input Section
    st.subheader("📝 Apna Safety Topic Dalein")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_input("Topic Name (e.g., Working at Height, Electrical Safety, Lifting):")
    with col2:
        language = st.selectbox("TBT Ki Bhasha (Language):", ["Hinglish (Simple Hindi + English)", "Pure Hindi", "English"])

    prompt = f"""
    You are an expert HSE Officer. Generate a professional, practical, and highly engaging Toolbox Talk (TBT) on the topic: '{topic}'.
    The language of the response must be strictly in {language}.
    
    Structure the response exactly like this:
    1. **Topic Title** (Bold)
    2. **Main Hazards (Khatre):** 3-4 bullet points of major risks.
    3. **Safe Work Practices (Suraksha ke Niyam):** 5-6 practical points for site workers.
    4. **PPE Required:** List of mandatory PPE.
    5. **5-Minute Summary/Slogan:** A short catchy line to ask workers at the end.
    """

    if st.button("🚀 AI Se TBT Content Generate Karein"):
        if not topic:
            st.error("Kripya koi topic likhein!")
        else:
            with st.spinner("⏳ AI aapka safety content taiyaar kar raha hai..."):
                try:
                    # Final stable model for 2026 standard
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                    
                    st.markdown("---")
                    st.success("🎉 Content Taiyaar Hai!")
                    st.markdown(response.text)
                    
                    st.download_button(
                        label="📄 Download TBT Notes",
                        data=response.text,
                        file_name=f"TBT_{topic.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error: {str(e)}")