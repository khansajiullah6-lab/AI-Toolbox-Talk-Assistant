import streamlit as str
import google.generativeai as genai

# Page Configuration
str.set_page_config(page_title="AI Toolbox Talk Assistant", layout="wide")

# Title and Description
str.title("📢 AI Toolbox Talk (TBT) Assistant")
str.write("Generate high-impact, customized 5-Minute Toolbox Talks instantly for heavy industries.")

# 🔑 API Key Logic
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

    # Sidebar Options
    str.sidebar.title("🛠️ Customization")
    language = str.sidebar.selectbox("Language Select Karein:", ["Hinglish", "Hindi", "English"])
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
                
                # Smart Multi-Model Fallback Logic (Taaki 404 Error bilkul na aaye)
                models_to_try = ['gemini-1.5-flash', 'gemini-pro', 'gemini-1.5-pro']
                response_text = None
                last_error = ""

                for model_name in models_to_try:
                    try:
                        model = genai.GenerativeModel(model_name)
                        response = model.generate_content(prompt)
                        response_text = response.text
                        if response_text:
                            break
                    except Exception as e:
                        last_error = str(e)
                        continue  # Agar ek model fail ho toh agla try karein

                if response_text:
                    str.success("✅ Aapka TBT Taiyaar Hai!")
                    str.markdown(response_text)
                    
                    # Download Button
                    str.download_button(
                        label="📄 Download TBT Notes",
                        data=response_text,
                        file_name=f"TBT_{topic.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    str.error(f"Google Gemini API error. Please check your API Key or try again later. Details: {last_error}")
        else:
            str.error("Kripya koi safety topic type karein!")
