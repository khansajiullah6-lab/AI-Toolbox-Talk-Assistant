import streamlit as str
import google.generativeai as genai

# Page Configuration
str.set_page_config(page_title="AI Toolbox Talk Assistant", layout="wide")

# Title and Description
str.title("📢 AI Toolbox Talk (TBT) Assistant")
str.write("Generate high-impact, customized 5-Minute Toolbox Talks instantly for heavy industries.")

# 🔑 API Key Logic (First check Streamlit Secrets, then check Sidebar)
api_key = None

if "GEMINI_API_KEY" in str.secrets:
    api_key = str.secrets["GEMINI_API_KEY"]
else:
    str.sidebar.title("🔑 AI Configuration")
    api_key = str.sidebar.text_input("Apni Google Gemini API Key yahan dalein:", type="password")

if not api_key:
    str.warning("⚠️ App chalane ke liye kripya left sidebar mein apni Gemini API Key dalein ya Streamlit Secrets mein set karein.")
else:
    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
model = genai.GenerativeModel('gemini-pro')
    # Sidebar Options
    str.sidebar.title("🛠️ Customization")
    language = str.sidebar.selectbox("Language Select Karein:", ["Hinglish", "Hindi", "English"])
    
    # Sector focus context
    sector = str.sidebar.selectbox("Sector / Project Type:", ["Mega Construction Project", "Oil & Gas Sector (Upstream/Downstream)", "General Industrial"])

    # Main Input
    topic = str.text_input("Safety Topic Yahan Type Karein (e.g., Working at Height, LOTO, H2S Safety):")

    if str.button("Generate TBT Points"):
        if topic:
            with str.spinner("AI aapke liye TBT taiyaar kar raha hai..."):
                prompt = f"""
                You are an expert HSE Manager in the {sector}. Generate a comprehensive 5-Minute Toolbox Talk (TBT) on the topic: '{topic}'.
                
                The response must be written strictly in the selected language: {language}.
                Format the output beautifully with clear headings and bullet points:
                
                1. Main Hazards (Khatre) - Specific to {sector}
                2. Safe Work Practices (Suraksha ke Niyam)
                3. Mandatory PPE Required
                4. A catchy, memorable 5-Minute Safety Slogan for site workers
                """
                
                try:
                    response = model.generate_content(prompt)
                    tbt_text = response.text
                    
                    str.success("✅ Aapka TBT Taiyaar Hai!")
                    str.markdown(tbt_text)
                    
                    # Download Button
                    str.download_button(
                        label="📄 Download TBT Notes",
                        data=tbt_text,
                        file_name=f"TBT_{topic.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    str.error(f"Error: {e}")
        else:
            str.error("Kripya koi safety topic type karein!")
