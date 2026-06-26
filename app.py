import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GA K-8 Math Framework Agent",
    page_icon="📐",
    layout="centered"
)

# --- INJECT CUSTOM COLORFUL MATH THEME ---
st.markdown("""
    <style>
    /* Main Background & Font Tweaks */
    .stApp {
        background-color: #f7fafc;
    }
    
    /* Hero Banner Box */
    .math-hero {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 30px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .math-hero h1 {
        color: #ffffff !important;
        font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
        font-size: 2.5rem !important;
        margin-bottom: 5px;
    }
    .math-hero p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Informational Feature Cards */
    .feature-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #3b82f6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .feature-card-title {
        font-weight: bold;
        color: #1e3a8a;
        font-size: 1.1rem;
        margin-bottom: 5px;
    }
    
    /* Styled Button Override */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: bold;
        padding: 10px 25px;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(16, 185, 129, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.title("控制 Control Panel")
password_input = st.sidebar.text_input("Enter App Password:", type="password")

# Automatically pull the API key securely from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")
authenticated = (password_input == st.secrets.get("PASSWORD", "Password123"))

def load_data():
    return pd.read_csv("ga_math_standards.csv")

# --- MAIN APP PORTAL ---
if not authenticated:
    st.markdown("""
        <div class="math-hero">
            <h1>📐 Math Framework Portal</h1>
            <p>Welcome, Educator! Please unlock the control panel to begin planning.</p>
        </div>
    """, unsafe_allow_html=True)
    st.info("👈 Enter your password in the sidebar to unlock the curriculum mapping generator.")
else:
    # Colorful Educational Header
    st.markdown("""
        <div class="math-hero">
            <h1>➕ GA Math Alignment Engine x²</h1>
            <p>Select your targeted elements below to instantly craft deep 4-step learning progressions.</p>
        </div>
    """, unsafe_allow_html=True)
    
    try:
        df = load_data()
        
        # Grid layout for selection filters using columns
        col1, col2 = st.columns(2)
        with col1:
            grades = sorted(df['Grade'].dropna().unique())
            selected_grade = st.selectbox("🎯 1. Target Grade:", grades)
            filtered_df = df[df['Grade'] == selected_grade]
            
            big_ideas = sorted(filtered_df['Big Idea'].dropna().unique())
            selected_big_idea = st.selectbox("💡 2. Big Idea:", big_ideas)
            filtered_df = filtered_df[filtered_df['Big Idea'] == selected_big_idea]
            
        with col2:
            main_standards = sorted(filtered_df['Standard'].dropna().unique())
            selected_main_standard = st.selectbox("🗂️ 3. Main Standard:", main_standards)
            filtered_df = filtered_df[filtered_df['Standard'] == selected_main_standard]

            sub_standards = sorted(filtered_df['Sub-Standard'].dropna().unique())
            selected_sub_standard = st.selectbox("🔍 4. Specific Target Element:", sub_standards)

        if selected_sub_standard:
            standard_desc = filtered_df[filtered_df['Sub-Standard'] == selected_sub_standard]['Description'].values[0]
            
            # Show standard inside a custom visual card
            st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-card-title">📍 Selected Focus Element: {selected_sub_standard}</div>
                    <div style="color: #4b5563;">{standard_desc}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # --- AI GENERATION LOGIC ---
            if not api_key:
                st.error("❌ The app couldn't find your GEMINI_API_KEY inside the Streamlit Secrets vault. Please double-check your Advanced Settings.")
            else:
                st.write("") # Spacer
                if st.button("✨ Generate 4-Step Teaching Sequence ✨"):
                    with st.spinner("Analyzing standards, clearing cognitive paths, and drafting tasks..."):
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
                                st.success(f"Sequence Successfully Generated!")
                                st.markdown("---")
                                st.markdown(response.text)
                            else:
                                st.error("Your API key is valid, but Google is reporting zero available text models.")
                                
                        except Exception as ai_error:
                            st.error(f"API Generation failed. Error details: {ai_error}")

    except Exception as e:
        st.error(f"Error reading CSV. Details: {e}")
