import streamlit as st
import google.generativeai as genai

# Import our custom standards dictionary instead of reading a CSV!
from standards import ga_standards

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Mr. Ward's GA Math Assistant",
    page_icon="📐",
    layout="centered"
)

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.title("Control Panel")
password_input = st.sidebar.text_input("Enter App Password:", type="password")

api_key = st.secrets.get("GEMINI_API_KEY", "")
authenticated = (password_input == st.secrets.get("PASSWORD", "Password123"))

# --- MAIN APP PORTAL ---
if not authenticated:
    st.markdown("""
        <style>
        /* The Custom Mesh Gradient Background */
        .stApp {
            background-color: #f0fdf4;
            background-image: 
                radial-gradient(at 80% 0%, #bbf7d0 0px, transparent 50%),
                radial-gradient(at 0% 50%, #fef08a 0px, transparent 50%),
                radial-gradient(at 80% 100%, #bfdbfe 0px, transparent 50%),
                radial-gradient(at 0% 0%, #e9d5ff 0px, transparent 50%);
            background-attachment: fixed;
        }
        /* Glassmorphism Banner */
        .math-hero {
            background: linear-gradient(135deg, rgba(30, 58, 138, 0.9) 0%, rgba(59, 130, 246, 0.9) 100%);
            backdrop-filter: blur(10px);
            padding: 30px; border-radius: 16px; color: white; text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); margin-bottom: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .math-hero h1 { color: white !important; font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif; font-size: 2.5rem !important; }
        </style>
        <div class="math-hero">
            <h1>📐 GA Math Assistant</h1>
            <p>Welcome, Educator! Please unlock the control panel to begin planning.</p>
        </div>
    """, unsafe_allow_html=True)
    st.info("👈 Enter your password in the sidebar to unlock the curriculum mapping generator.")
else:
    try:
        # Load grades from our custom Python dictionary
        grades = list(ga_standards.keys())
        
        col1, col2 = st.columns(2)
        with col1:
            selected_grade = st.selectbox("🎯 1. Target Grade:", grades)
            main_standards = list(ga_standards[selected_grade].keys())
            selected_main_standard = st.selectbox("🗂️ 2. Main Standard:", main_standards)
            
        with col2:
            sub_standards = ga_standards[selected_grade][selected_main_standard]
            selected_sub_standard = st.selectbox("🔍 3. Specific Target Element:", sub_standards)

        # --- DYNAMIC GRADE-BAND THEMING ENGINE ---
        if selected_grade in ['Kindergarten', '1st Grade', '2nd Grade']:
            primary_gradient = "linear-gradient(135deg, rgba(245, 158, 11, 0.9) 0%, rgba(217, 119, 6, 0.9) 100%)"
            accent_color = "#d97706"
            btn_gradient = "linear-gradient(135deg, #f59e0b 0%, #b45309 100%)"
        elif selected_grade in ['3rd Grade', '4th Grade', '5th Grade']:
            primary_gradient = "linear-gradient(135deg, rgba(16, 185, 129, 0.9) 0%, rgba(4, 120, 87, 0.9) 100%)"
            accent_color = "#047857"
            btn_gradient = "linear-gradient(135deg, #10b981 0%, #064e3b 100%)"
        else: # 6th, 7th, 8th Grade
            primary_gradient = "linear-gradient(135deg, rgba(30, 58, 138, 0.9) 0%, rgba(59, 130, 246, 0.9) 100%)"
            accent_color = "#1e3a8a"
            btn_gradient = "linear-gradient(135deg, #10b981 0%, #059669 100%)"

        st.markdown(f"""
            <style>
            /* The Custom Mesh Gradient Background for Main App */
            .stApp {{
                background-color: #f0fdf4;
                background-image: 
                    radial-gradient(at 80% 0%, #bbf7d0 0px, transparent 50%),
                    radial-gradient(at 0% 50%, #fef08a 0px, transparent 50%),
                    radial-gradient(at 80% 100%, #bfdbfe 0px, transparent 50%),
                    radial-gradient(at 0% 0%, #e9d5ff 0px, transparent 50%);
                background-attachment: fixed;
            }}
            
            /* Glassmorphism Header Card */
            .math-hero {{
                background: {primary_gradient};
                backdrop-filter: blur(10px);
                padding: 30px; border-radius: 16px; color: white; text-align: center;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin-bottom: 25px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            .math-hero h1 {{
                color: #ffffff !important;
                font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
                font-size: 2.5rem !important; margin-bottom: 5px;
            }}
            
            /* Frosted Glass Feature Cards */
            .feature-card {{
                background-color: rgba(255, 255, 255, 0.7);
                backdrop-filter: blur(12px);
                padding: 20px; border-radius: 12px;
                border-left: 6px solid {accent_color};
                border-right: 1px solid rgba(255, 255, 255, 0.5);
                border-top: 1px solid rgba(255, 255, 255, 0.5);
                border-bottom: 1px solid rgba(255, 255, 255, 0.5);
                box-shadow: 0 8px 32px rgba(0,0,0,0.05); margin-top: 10px; margin-bottom: 20px;
            }}
            .feature-card-title {{ font-weight: bold; color: {accent_color}; font-size: 1.1rem; margin-bottom: 5px; }}
            
            /* Master Action Button */
            div.stButton > button:first-child {{
                background: {btn_gradient};
                color: white !important; font-size: 1.2rem !important; font-weight: bold;
                padding: 12px 25px; border-radius: 8px; border: none;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: all 0.3s ease; width: 100%;
            }}
            div.stButton > button:first-child:hover {{
                transform: translateY(-2px); box-shadow: 0 6px 18px rgba(0,0,0,0.15);
            }}
            
            /* AI Output Step Cards */
            .lesson-step-card {{
                background-color: rgba(255, 255, 255, 0.85);
                backdrop-filter: blur(10px);
                border-radius: 10px; padding: 20px; margin-bottom: 20px; 
                box-shadow: 0 8px 32px rgba(0,0,0,0.05);
                border: 1px solid rgba(255, 255, 255, 0.6);
            }}
            .step-header {{
                font-size: 1.3rem !important; font-weight: bold !important;
                margin-bottom: 12px !important; padding-bottom: 6px;
                border-bottom: 2px solid #e2e8f0;
            }}
            .sh-1 {{ color: #ef4444; border-image: linear-gradient(to right, #ef4444, rgba(0,0,0,0)) 1; }}
            .sh-2 {{ color: #3b82f6; border-image: linear-gradient(to right, #3b82f6, rgba(0,0,0,0)) 1; }}
            .sh-3 {{ color: #f59e0b; border-image: linear-gradient(to right, #f59e0b, rgba(0,0,0,0)) 1; }}
            .sh-4 {{ color: #8b5cf6; border-image: linear-gradient(to right, #8b5cf6, rgba(0,0,0,0)) 1; }}
            .sh-5 {{ color: #ec4899; border-image: linear-gradient(to right, #ec4899, rgba(0,0,0,0)) 1; }}
            
            /* Make Streamlit Dropdowns slightly transparent to match */
            div[data-baseweb="select"] > div {{
                background-color: rgba(255, 255, 255, 0.7) !important;
                backdrop-filter: blur(5px);
            }}
            </style>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="math-hero">
                <h1>➕ Mr. Ward's GA Math Assistant</h1>
                <p>Select your targeted elements below to instantly craft deep learning progressions.</p>
            </div>
        """, unsafe_allow_html=True)

        if selected_sub_standard:
            st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-card-title">📍 Selected Focus Element: {selected_sub_standard}</div>
                    <div style="color: #4b5563;">Developing a mastery sequence for {selected_sub_standard} under the domain: {selected_main_standard}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if not api_key:
                st.error("❌ The app couldn't find your GEMINI_API_KEY inside the Streamlit Secrets vault. Please double-check your Advanced Settings.")
            else:
                st.write("") 
                if st.button("✨ Generate Master Teaching Sequence ✨"):
                    with st.spinner("Analyzing standards, clearing cognitive paths, and drafting tasks..."):
                        try:
                            clean_key = api_key.strip()
                            genai.configure(api_key=clean_key)
                            
                            # Using the current, reliable fast model
                            model = genai.GenerativeModel("gemini-2.5-flash")
                            
                            prompt = f"""
                            You are an expert master teacher and curriculum designer for Georgia K-8 Math.
                            Analyze this specific standard: {selected_sub_standard} from the domain: {selected_main_standard}.
                            
                            Output a strict, highly engaging 5-step teaching progression for this standard.
                            You MUST wrap each step exactly in the provided HTML block formatting below so it renders as visual cards. Do not use generic markdown headers.
                            
                            <div class="lesson-step-card">
                            <div class="step-header sh-1">1. Concrete/Visual Hook</div>
                            [Provide a clear, hands-on, real-world introduction using physical objects, visuals, or conceptual scenarios appropriate for this grade level. Use bullet points.]
                            </div>

                            <div class="lesson-step-card">
                            <div class="step-header sh-2">2. Direct Modeling (The Big Idea)</div>
                            [Explain step-by-step how to explicitly teach and demonstrate the core mathematical concept to build deep conceptual understanding. Use bullet points.]
                            </div>

                            <div class="lesson-step-card">
                            <div class="step-header sh-3">3. Assessment Rigor (Milestones Prep)</div>
                            [Generate three highly targeted questions that perfectly mirror the formatting and rigor of state testing: 1 Multiple-Choice, 1 Multi-Select, and 1 Short Constructed Response. Include a clear, bolded Answer Key at the bottom of this card.]
                            </div>

                            <div class="lesson-step-card">
                            <div class="step-header sh-4">4. Interactive Game Design</div>
                            [Design a creative, interactive math game tailored to this standard that can be built physically or played in class. Specify the Core Mechanics, Win Conditions, and Materials needed.]
                            </div>

                            <div class="lesson-step-card">
                            <div class="step-header sh-5">5. If the Students Still Don't Understand</div>
                            [Identify the absolute biggest conceptual misconception or stumbling block students face with this specific standard. Provide an immediate, alternative backup strategy/remediation path to reach struggling learners.]
                            </div>

                            Do not include any introductory or concluding text. Return only the 5 HTML blocks.
                            """
                            
                            response = model.generate_content(prompt)
                            st.success(f"Sequence Successfully Generated!")
                            st.markdown("---")
                            
                            # Clean the AI output to remove markdown code blocks
                            clean_text = response.text.replace("```html", "").replace("```", "").strip()
                            st.markdown(clean_text, unsafe_allow_html=True)
                            
                        except Exception as ai_error:
                            st.error(f"API Generation failed. Error details: {ai_error}")

    except Exception as e:
        st.error(f"Error loading standards data. Please ensure 'standards.py' is saved correctly in your repository. Details: {e}")
