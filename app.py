import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="GA Math Agent", layout="centered")

# --- SIDEBAR: ACCESS CONTROL ---
with st.sidebar:
    st.header("⚙️ Agent Settings")
    user_password = st.text_input("Enter Password:", type="password")
    
    # Safely look for secrets so your local computer doesn't crash
    try:
        secret_password = st.secrets["PASSWORD"]
        secret_api_key = st.secrets["GEMINI_API_KEY"]
    except:
        secret_password = "local" # Fallback so the app doesn't break on your desktop
        secret_api_key = ""
        
    # Check if the password matches (using .strip() to ignore accidental phone spaces)
    if user_password.strip() == secret_password:
        api_key = secret_api_key
        st.success("Access Granted!")
        authenticated = True
    else:
        api_key = ""
        authenticated = False
        if user_password != "":
            st.error("Incorrect Password")

def load_data():
    return pd.read_csv("ga_math_standards.csv")

# --- MAIN APP GATEKEEPER ---
if not authenticated:
    st.title("🔒 Georgia K-8 Math Framework Agent")
    st.info("Please enter the password in the sidebar to unlock the application.")
else:
    st.title("🤖 GA K-8 Math Framework Agent")
    st.write("Select a standard to generate a dynamic teaching sequence.")
    
    try:
        df = load_data()
        
        # 1. Grade Dropdown
        grades = sorted(df['Grade'].dropna().unique())
        selected_grade = st.selectbox("1. Choose Grade Level:", grades)
        filtered_df = df[df['Grade'] == selected_grade]
        
        # 2. Big Idea Dropdown
        big_ideas = sorted(filtered_df['Big Idea'].dropna().unique())
        selected_big_idea = st.selectbox("2. Choose Big Idea:", big_ideas)
        filtered_df = filtered_df[filtered_df['Big Idea'] == selected_big_idea]
        
        # 3. Main Standard Dropdown (NEW)
        main_standards = sorted(filtered_df['Standard'].dropna().unique())
        selected_main_standard = st.selectbox("3. Choose Main Standard:", main_standards)
        filtered_df = filtered_df[filtered_df['Standard'] == selected_main_standard]

        # 4. Sub-Standard Dropdown (NEW)
        sub_standards = sorted(filtered_df['Sub-Standard'].dropna().unique())
        selected_sub_standard = st.selectbox("4. Choose Specific Sub-Standard:", sub_standards)

        if selected_sub_standard:
            standard_desc = filtered_df[filtered_df['Sub-Standard'] == selected_sub_standard]['Description'].values[0]
            st.markdown("---")
            st.subheader(f"{selected_sub_standard}")
            st.write(f"**Description:** {standard_desc}")
            
            # --- AI GENERATION LOGIC ---
            if not api_key:
                st.warning("👈 Missing API Key from the secret vault.")
            else:
                if st.button("Generate Teaching Sequence"):
                    with st.spinner("Agent is diagnosing servers and designing the sequence..."):
                        try:
                            clean_key = api_key.strip()
                            genai.configure(api_key=clean_key)
                            
                            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                            
                            if available_models:
                                chosen_model = available_models[0].replace('models/', '')
                                model = genai.GenerativeModel(chosen_model)
                                
                                prompt = f"""
                                You are an expert master teacher and curriculum designer for Georgia K-8 Math.
                                Analyze this specific standard: {selected_sub_standard} - {standard_desc}
                                
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
