import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="GA Math Agent", layout="centered")

# --- SIDEBAR: API KEY INPUT ---
with st.sidebar:
    st.header("⚙️ Agent Settings")
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    default_key = st.secrets.get("GEMINI_API_KEY", "")
api_key = st.text_input("Enter your Gemini API Key:", value=default_key, type="password")
st.write("Select a standard to generate a dynamic teaching sequence.")

@st.cache_data
def load_data():
    return pd.read_csv("ga_math_standards.csv")

try:
    df = load_data()
    
    # Dropdowns
    grades = sorted(df['Grade'].dropna().unique())
    selected_grade = st.selectbox("1. Choose Grade Level:", grades)

    filtered_df = df[df['Grade'] == selected_grade]
    
    big_ideas = sorted(filtered_df['Big Idea'].dropna().unique())
    selected_big_idea = st.selectbox("2. Choose Big Idea:", big_ideas)

    filtered_df = filtered_df[filtered_df['Big Idea'] == selected_big_idea]
    
    standards = sorted(filtered_df['Standard Code'].dropna().unique())
    selected_standard = st.selectbox("3. Choose Standard:", standards)

    if selected_standard:
        standard_desc = filtered_df[filtered_df['Standard Code'] == selected_standard]['Standard Description'].values[0]
        st.markdown("---")
        st.subheader(f"{selected_standard}")
        st.write(f"**Description:** {standard_desc}")
        
        # --- AI GENERATION LOGIC ---
        if not api_key:
            st.warning("👈 Please enter your Gemini API key in the sidebar to generate the sequence.")
        else:
            if st.button("Generate Teaching Sequence"):
                with st.spinner("Agent is diagnosing servers and designing the sequence..."):
                    try:
                        # 1. Clean the key (removes accidental spaces from copy/pasting)
                        clean_key = api_key.strip()
                        genai.configure(api_key=clean_key)
                        
                        # 2. Force the API to give us the exact models it supports for your key
                        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                        
                        # 3. Grab the first valid model automatically
                        if available_models:
                            chosen_model = available_models[0].replace('models/', '')
                            
                            model = genai.GenerativeModel(chosen_model)
                            
                            # The strict instructional prompt
                            prompt = f"""
                            You are an expert master teacher and curriculum designer for Georgia K-8 Math.
                            Analyze this specific standard: {selected_standard} - {standard_desc}
                            
                            Output a strict, highly engaging 4-step teaching progression for this standard:
                            1. Concrete/Visual Hook
                            2. Direct Modeling (The Big Idea)
                            3. Guided Practice (Algorithmic)
                            4. Performance Task (Gamified)
                            
                            Keep it concise, formatting it beautifully with bold headers and bullet points. Do not include introductory fluff.
                            """
                            
                            response = model.generate_content(prompt)
                            st.success(f"Sequence Generated using: {chosen_model}")
                            st.markdown(response.text)
                        else:
                            st.error("Your API key is valid, but Google is reporting zero available text models for it right now.")
                            
                    except Exception as ai_error:
                        st.error(f"API Generation failed. Error details: {ai_error}")

except Exception as e:
    st.error(f"Error reading CSV. Details: {e}")
