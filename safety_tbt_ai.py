import streamlit as st
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(page_title="AI Toolbox Talk Assistant", layout="wide")

# Title and Description
st.title("📢 AI Toolbox Talk (TBT) Assistant")
st.write("Generate high-impact, customized 5-Minute Toolbox Talks instantly for heavy industries.")

# 🔑 API Key Logic
api_key = None

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.sidebar.title("🔑 AI Configuration")
    api_key = st.sidebar.text_input("Apni Google Gemini API Key yahan dalein:", type="password")

if not api_key:
    st.warning("⚠️ App chalane ke liye kripya left sidebar mein apni Gemini API Key dalein ya Streamlit Secrets mein set karein.")
else:
    try:
        # Initialize the new Google GenAI Client
        client = genai.Client(api_key=api_key)

        # Sidebar Options
        st.sidebar.title("🛠️ Customization")
        language = st.sidebar.selectbox("Language Select Karein:", ["Hinglish", "Hindi", "English"])
        sector = st.sidebar.selectbox("Sector / Project Type:", ["Mega Construction Project", "Oil & Gas Sector (Upstream/Downstream)", "General Industrial"])

        # Main Input
        topic = st.text_input("Safety Topic Yahan Type Karein (e.g., Working at Height, LOTO, H2S Safety):")

        if st.button("Generate TBT Points"):
            if topic:
                with st.spinner("AI aapke liye TBT taiyaar kar raha hai..."):
                    prompt = f"""
                    You are an expert HSE Manager in the {sector}. Generate a comprehensive 5-Minute Toolbox Talk (TBT) on the topic: '{topic}'.
                    
                    The response must be written strictly in the selected language: {language}.
                    Format the output beautifully with clear headings and bullet points:
                    
                    1. Main Hazards (Khatre) - Specific to {sector}
                    2. Safe Work Practices (Suraksha ke Niyam)
                    3. Mandatory PPE Required
                    4. A catchy, memorable 5-Minute Safety Slogan for site workers
                    """
                    
                    # Using the latest universal model that works on all accounts
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                    
                    tbt_text = response.text
                    
                    if tbt_text:
                        st.success("✅ Aapka TBT Taiyaar Hai!")
                        st.markdown(tbt_text)
                        
                        # Download Button
                        st.download_button(
                            label="📄 Download TBT Notes",
                            data=tbt_text,
                            file_name=f"TBT_{topic.replace(' ', '_')}.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("AI se koi response nahi mila. Kripya dobara try karein.")
            else:
                st.error("Kripya koi safety topic type karein!")
                
    except Exception as e:
        st.error(f"App Execution Error: {e}")
