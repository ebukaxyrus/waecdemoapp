import streamlit as st
import pandas as pd
import os
import re
from openai import OpenAI
from gtts import gTTS
import base64
import time

# Configure the Streamlit page with custom CSS
st.set_page_config(
    page_title="WAEC English Mastery",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern UI design matching the image
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
   
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%);
        min-height: 100vh;
        padding: 0;
        color: #1f2937;
    }

    .stApp {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 50%, #1d4ed8 100%);
    }
   
    /* Main Container */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        margin-top: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
   
    /* Header Section */
    .app-header {
        text-align: center;
        padding: 2rem 1rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    }

    .app-header h1 {
        color: #1e293b;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .app-header p {
        color: #64748b;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }

    /* Stats Cards Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }

    .stat-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }

    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        color: #3b82f6;
        margin-bottom: 0.5rem;
    }

    .stat-label {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Progress Bar */
    .progress-container {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 0.5rem;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }

    .progress-bar {
        background: linear-gradient(90deg, #3b82f6, #1e40af);
        height: 16px;
        border-radius: 8px;
        transition: width 0.5s ease;
        box-shadow: 0 2px 10px rgba(79, 70, 229, 0.4);
    }

    .progress-text {
        text-align: center;
        color: white;
        margin-top: 0.5rem;
        font-weight: 600;
        font-size: 0.9rem;
    }

    /* Question Card */
    .question-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        border-radius: 24px;
        padding: 2rem;
        margin: 2rem 0;
        color: #1e293b;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .question-header {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1rem;
        display: inline-block;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }

    .question-text {
        font-size: 1.25rem;
        font-weight: 600;
        line-height: 1.6;
        margin-bottom: 2rem;
        color: #1e293b;
    }

    /* Options Styling */
    .option-container {
        margin: 1rem 0;
    }

    .stRadio > div {
        gap: 0.8rem;
    }

    .stRadio > div > label {
        background: rgba(79, 70, 229, 0.05) !important;
        border: 2px solid rgba(79, 70, 229, 0.2) !important;
        border-radius: 16px !important;
        padding: 1.2rem 1.5rem !important;
        margin: 0.5rem 0 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #1e293b !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }

    .stRadio > div > label:hover {
        background: rgba(79, 70, 229, 0.1) !important;
        border-color: rgba(79, 70, 229, 0.4) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.2) !important;
    }

    /* Action Buttons */
    .button-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }

    .stButton > button {
        width: 100% !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        border: none !important;
        cursor: pointer !important;
        text-transform: none !important;
    }

    /* Primary Button */
    .primary-btn button {
        background: linear-gradient(135deg, #3b82f6, #1e40af) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3) !important;
    }

    .primary-btn button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4) !important;
    }

    /* Secondary Button */
    .secondary-btn button {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #4f46e5 !important;
        border: 2px solid rgba(79, 70, 229, 0.3) !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
    }

    .secondary-btn button:hover {
        background: rgba(255, 255, 255, 1) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
    }

    /* Skip Button */
    .skip-btn button {
        background: rgba(251, 146, 60, 0.1) !important;
        color: #f59e0b !important;
        border: 2px solid rgba(251, 146, 60, 0.3) !important;
    }

    .skip-btn button:hover {
        background: rgba(251, 146, 60, 0.2) !important;
        transform: translateY(-2px) !important;
    }

    /* Success/Error Messages */
    .success-card {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
    }

    .error-card {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3);
    }

    /* Explanation Card */
    .explanation-card {
        background: linear-gradient(135deg, #06b6d4, #0891b2);
        color: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(6, 182, 212, 0.3);
    }

    .explanation-card h3 {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    /* Passage Container */
    .passage-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .passage-card h3 {
        color: white;
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }

    .passage-text {
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.7;
        font-size: 1rem;
    }

    /* Year Selector */
    .year-selector {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 0.3rem;
        margin-bottom: 1rem;
        text-align: center;
    }
                
    

    .year-selector h3 {
        color: #1e293b;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    /* Final Results */
    .final-results {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        padding: 3rem 2rem;
        margin: 3rem 0;
        text-align: center;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
    }

    .final-results h2 {
        color: #1e293b;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .performance-message {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 2rem 0;
        padding: 1.5rem;
        border-radius: 16px;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 3rem 1rem;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 4rem;
    }

    .app-footer p {
        margin: 0.5rem 0;
        font-weight: 500;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main-container {
            margin: 1rem;
            padding: 0.5rem;
        }
        
        .app-header h1 {
            font-size: 2rem;
        }
        
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 0.8rem;
        }
        
        .stat-card {
            padding: 1rem;
        }
        
        .stat-value {
            font-size: 1.5rem;
        }
        
        .question-card {
            padding: 1.5rem;
        }
        
        .question-text {
            font-size: 1.1rem;
        }
        
        .button-container {
            grid-template-columns: repeat(2, 1fr);
            gap: 0.8rem;
        }
    }

    @media (max-width: 480px) {
        .stats-grid {
            grid-template-columns: 1fr;
        }
        
        .button-container {
            grid-template-columns: 1fr;
        }
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
                
    
                
        /* Keep sidebar open and position toggle correctly */
    section[data-testid="stSidebar"] {
        min-width: 280px !important;
        width: 280px !important;
    }

    /* Position the toggle button outside */
    section[data-testid="stSidebar"] > div:first-child {
        position: relative;
    }

    button[data-testid="collapsedControl"] {
        position: absolute !important;
        right: -12px !important;
        top: 10px !important;
        z-index: 999 !important;
    }

    /* Hide the collapse button */
    button[data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(79, 70, 229, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(79, 70, 229, 0.7);
    }
                
    
    </style>
    """, unsafe_allow_html=True)

# Load custom CSS
load_css()

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h2 style="color: white; margin-bottom: 1rem;">📅 Select Year</h2>
    </div>
    """, unsafe_allow_html=True)
   
    selected_year = st.selectbox(
        "Choose exam year:",
        list(range(2024, 2014, -1)),
        key="year_select"
    )

        # In your sidebar section, add:
    st.markdown("### 🎵 Voice Settings")
    selected_voice = st.selectbox(
        "Choose TTS voice:",
        ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
        key="voice_select"
    )
   
    st.markdown("---")
   
    # Quick Stats in Sidebar
    if "year_data" in st.session_state and selected_year in st.session_state.year_data:
        year_data = st.session_state.year_data[selected_year]
        attempted_questions = len([k for k, v in year_data.get("attempted", {}).items() if v != "SKIPPED"])
       
        st.markdown(f"""
        <div style="text-align: center; color: white;">
            <h3>📊 Quick Stats</h3>
            <p><strong>Score:</strong> {year_data.get('score', 0)}/{attempted_questions}</p>
            <p><strong>Progress:</strong> {year_data.get('index', 0) + 1} questions</p>
        </div>
        """, unsafe_allow_html=True)

# Add this after your sidebar code, before main container


# --- API Configuration ---
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")

client = None
if OPENAI_API_KEY and OPENAI_API_KEY.startswith("sk-"):
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception as e:
        st.error(f"❌ Error initializing OpenAI client: {e}")
else:
    st.warning("🔑 Please provide a valid OpenAI API key to enable AI explanations")

# Helper Functions
def format_question_text(text):
    if pd.isna(text) or not text:
        return ""
    text = str(text).strip()
    text = re.sub(r'_([^_]+)_', r'<u>\1</u>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    return text

def clean_option_text(text):
    if pd.isna(text) or not text:
        return "Option missing"
    text = str(text).strip()
    text = re.sub(r'^[A-D]\.\s*', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text if text else "Option missing"

def generate_audio_file_openai(explanation_text, file_path):
    if not client:
        st.warning("⚠️ OpenAI client not available for TTS.")
        return None
        
    try:
        if not explanation_text or explanation_text.strip() == "":
            st.warning("⚠️ No text to convert to speech.")
            return None
            
        response = client.audio.speech.create(
            model="tts-1",  # or "tts-1-hd" for higher quality
            voice=selected_voice,  # Options: alloy, echo, fable, onyx, nova, shimmer
            input=explanation_text
        )
        
        # Save the audio file
        response.stream_to_file(file_path)
        return file_path
        
    except Exception as e:
        st.error(f"❌ Error generating audio with OpenAI TTS: {str(e)}")
        return None

def generate_ai_explanation(question, options, correct_answer, selected_answer, question_type, passage_text=None):
    if not client:
        return "🔑 AI explanations unavailable - API key not configured."
   
    try:
        context = f"Question: {question}\n"
        context += f"A. {options.get('A', '')}\nB. {options.get('B', '')}\nC. {options.get('C', '')}\nD. {options.get('D', '')}\n"
        context += f"Correct Answer: {correct_answer}\nStudent's Answer: {selected_answer}\n"
       
        if passage_text and question_type in ["comprehension", "passage"]:
            context += f"Passage: {passage_text[:400]}...\n"
       
        if selected_answer == correct_answer:
            prompt = f"""The student got this WAEC English question correct. Provide a brief explanation (2-3 sentences max) for a 15-18 year old student explaining why option {correct_answer} is the right answer.

{context}

Keep it encouraging and educational."""
        else:
            prompt = f"""The student got this WAEC English question wrong. Provide a brief explanation (2-3 sentences max) for a 15-18 year old student explaining why option {correct_answer} is correct and why their choice ({selected_answer}) was incorrect.

{context}
#max_tokens=120,temperature=0.7
Be encouraging and help them learn from the mistake."""

        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "You are a helpful English teacher providing brief, clear explanations for WAEC students. Keep responses short and encouraging."},
                {"role": "user", "content": prompt}
            ]

            
            
        )
       
        return response.choices[0].message.content.strip()
   
    except Exception as e:
        return f"❌ Error generating explanation: {str(e)[:100]}..."

def find_passage_for_question(original_df, current_q_original_num):
    if pd.isna(current_q_original_num):
        return None, False

    passage_text = None
    potential_passages = original_df[
        original_df['Question_Type'].isin(['comprehension', 'passage']) &
        original_df['OptionA'].isna() &
        original_df['OptionB'].isna() &
        original_df['OptionC'].isna() &
        original_df['OptionD'].isna()
    ].copy()

    potential_passages['Question_Number'] = pd.to_numeric(potential_passages['Question_Number'], errors='coerce')
    potential_passages = potential_passages.dropna(subset=['Question_Number'])
    potential_passages = potential_passages.sort_values(by='Question_Number', ascending=True)

    for _, row in potential_passages.iterrows():
        passage_q_num = row.get("Question_Number", float('-inf'))
        if not pd.isna(passage_q_num) and passage_q_num <= current_q_original_num:
            passage_text = row['Question']
        elif not pd.isna(passage_q_num) and passage_q_num > current_q_original_num:
            break
           
    return (passage_text, False) if passage_text else (None, True)

@st.cache_data
def load_data(selected_year):
    filename = f"waec_english_{selected_year}_complete.csv"
    if not os.path.exists(filename):
        st.error(f"❌ File '{filename}' not found.")
        st.stop()
   
    try:
        df = pd.read_csv(filename)
    except Exception as e:
        st.error(f"❌ Error reading CSV file: {e}")
        st.stop()

    if df.empty:
        st.error("❌ CSV file is empty.")
        st.stop()
   
    required = ["Question", "OptionA", "OptionB", "OptionC", "OptionD", "Answer", "Question_Number", "Question_Type"]
    missing_cols = [col for col in required if col not in df.columns]
    if missing_cols:
        st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
        st.stop()
   
    st.session_state.original_df = df.copy()
    df_filtered = df.dropna(subset=["Question", "Answer"])
    df_filtered = df_filtered[df_filtered["Answer"].str.strip().isin(["A", "B", "C", "D"])]
   
    for opt in ["OptionA", "OptionB", "OptionC", "OptionD"]:
        df_filtered[opt] = df_filtered[opt].fillna(f"{opt[-1]} option missing")
   
    return df_filtered.reset_index(drop=True)

# Main App Container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Year Selection at the top


# Initialize year-specific session state
if "year_data" not in st.session_state:
    st.session_state.year_data = {}

if selected_year not in st.session_state.year_data:
    st.session_state.year_data[selected_year] = {
        "index": 0,
        "score": 0,
        "submitted": False,
        "attempted": {},
        "show_explanation": False,
        "explanations": {}
    }

# Handle year change
if "current_year" not in st.session_state:
    st.session_state.current_year = selected_year
elif st.session_state.current_year != selected_year:
    if st.session_state.current_year in st.session_state.year_data:
        st.session_state.year_data[st.session_state.current_year].update({
            "index": st.session_state.get("index", 0),
            "score": st.session_state.get("score", 0),
            "submitted": st.session_state.get("submitted", False),
            "attempted": st.session_state.get("attempted", {}),
            "show_explanation": st.session_state.get("show_explanation", False),
            "explanations": st.session_state.get("explanations", {})
        })
   
    st.session_state.current_year = selected_year
    year_data = st.session_state.year_data[selected_year]
    st.session_state.index = year_data["index"]
    st.session_state.score = year_data["score"]
    st.session_state.submitted = year_data["submitted"]
    st.session_state.attempted = year_data["attempted"]
    st.session_state.show_explanation = year_data["show_explanation"]
    st.session_state.explanations = year_data.get("explanations", {})
    st.rerun()

# Load data
df = load_data(selected_year)

# Session state initialization
if "index" not in st.session_state:
    st.session_state.index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "attempted" not in st.session_state:
    st.session_state.attempted = {}
if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False
if "explanations" not in st.session_state:
    st.session_state.explanations = {}


# Ensure valid index
if len(df) == 0:
    st.warning("No questions found for the selected year.")
    st.stop()

if st.session_state.index >= len(df):
    st.session_state.index = 0
    st.session_state.submitted = False

# Navigation functions
def save_current_state():
    if st.session_state.current_year in st.session_state.year_data:
        st.session_state.year_data[st.session_state.current_year].update({
            "index": st.session_state.index,
            "score": st.session_state.score,
            "submitted": st.session_state.submitted,
            "attempted": st.session_state.attempted,
            "show_explanation": st.session_state.show_explanation,
            "explanations": st.session_state.explanations
        })

def go_next():
    if st.session_state.index < len(df) - 1:
        st.session_state.index += 1
        st.session_state.submitted = st.session_state.index in st.session_state.attempted
        st.session_state.show_explanation = False
        save_current_state()
    st.rerun()

def go_prev():
    if st.session_state.index > 0:
        st.session_state.index -= 1
        st.session_state.submitted = st.session_state.index in st.session_state.attempted
        st.session_state.show_explanation = False
        save_current_state()
    st.rerun()

# Main Application UI
try:
    q = df.iloc[st.session_state.index]
    question_type = q.get("Question_Type", "").lower()

    # Header
    st.markdown(f"""
    <div class="app-header">
        <h1>🎓 WAEC English Mastery</h1>
        <p>AI-Enhanced Learning Platform • {selected_year} Edition</p>
    </div>
    """, unsafe_allow_html=True)

    # Progress Stats
    attempted_for_score = [k for k, v in st.session_state.attempted.items() if v != "SKIPPED"]
    skipped_count = len([k for k, v in st.session_state.attempted.items() if v == "SKIPPED"])
    accuracy = (st.session_state.score / len(attempted_for_score)) * 100 if attempted_for_score else 0
    progress = (st.session_state.index + 1) / len(df) * 100

    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">{st.session_state.score}/{len(attempted_for_score)}</div>
            <div class="stat-label">Score</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{accuracy:.1f}%</div>
            <div class="stat-label">Accuracy</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{st.session_state.index + 1}/{len(df)}</div>
            <div class="stat-label">Questions</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{skipped_count}</div>
            <div class="stat-label">Skipped</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Progress Bar
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress}%;"></div>
        <div class="progress-text">Progress: {progress:.1f}% Complete</div>
    </div>
    """, unsafe_allow_html=True)

    # Show passage for comprehension questions
    passage_text = None
    if question_type in ["comprehension", "passage"]:
        if hasattr(st.session_state, 'original_df') and not st.session_state.original_df.empty:
            current_q_original_num = q.get("Question_Number", None)
            passage_text, is_missing = find_passage_for_question(
                st.session_state.original_df,
                current_q_original_num
            )
           
            if passage_text:
                st.markdown(f"""
                <div class="passage-card">
                    <h3>📘 Comprehension Passage</h3>
                    <div class="passage-text">
                        {format_question_text(passage_text)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Question Card
    st.markdown(f"""
    <div class="question-card">
        <div class="question-header">Question {st.session_state.index + 1} of {len(df)}</div>
        <div class="question-text">{format_question_text(q['Question'])}</div>
    """, unsafe_allow_html=True)

    # Prepare options
    options, display_opts = {}, {}
    for opt_char in ["A", "B", "C", "D"]:
        key = f"Option{opt_char}"
        val = clean_option_text(q[key])
        options[opt_char] = val
        display_opts[opt_char] = f"{opt_char}. {val}"

    # Answer selection
    stored_answer = st.session_state.attempted.get(st.session_state.index, None)
    radio_index = None
    if stored_answer in options and st.session_state.index in st.session_state.attempted:
        try:
            radio_index = list(options.keys()).index(stored_answer)
        except ValueError:
            radio_index = None

    selected = st.radio(
        "Choose your answer:",
        list(options.keys()),
        format_func=lambda x: display_opts[x],
        key=f"q_radio_{st.session_state.index}_{selected_year}",
        index=radio_index,
        label_visibility="collapsed"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Action Buttons
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("⬅️ Previous", disabled=st.session_state.index == 0, key="prev_btn"):
            go_prev()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        submit_disabled = selected is None or st.session_state.submitted
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("✅ Submit", disabled=submit_disabled, key="submit_btn"):
            if not st.session_state.submitted:
                st.session_state.attempted[st.session_state.index] = selected
                correct = q["Answer"].strip().upper()
                if selected == correct:
                    st.session_state.score += 1
                    st.markdown(f'<div class="success-card">🎉 Excellent! You selected {selected}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="error-card">💪 Good try! You chose {selected}. Correct answer: {correct}</div>', unsafe_allow_html=True)
                st.session_state.submitted = True
                if client:
                    st.session_state.show_explanation = True
                save_current_state()
                time.sleep(5)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        if st.session_state.index not in st.session_state.attempted or st.session_state.attempted[st.session_state.index] == "SKIPPED":
            st.markdown('<div class="skip-btn">', unsafe_allow_html=True)
            if st.button("⏭️ Skip", key="skip_btn"):
                st.session_state.attempted[st.session_state.index] = "SKIPPED"
                st.session_state.submitted = True
                st.session_state.show_explanation = False
                save_current_state()
                go_next()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="skip-btn">', unsafe_allow_html=True)
            st.button("⏭️ Skip", disabled=True, key="skip_btn_disabled")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        next_disabled = (st.session_state.index == len(df) - 1) or \
                        (not st.session_state.submitted and not (st.session_state.index in st.session_state.attempted))
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("➡️ Next", disabled=next_disabled, key="next_btn"):
            go_next()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Show results and explanations
    if st.session_state.submitted and st.session_state.index in st.session_state.attempted:
        ans = st.session_state.attempted[st.session_state.index]
        if ans != "SKIPPED" and ans in options:
            correct = q["Answer"].strip().upper()
           
            # Generate AI explanation if available
            if client:
                explanation_key = f"{st.session_state.index}_{selected_year}"
               
                if explanation_key not in st.session_state.explanations:
                    with st.spinner("🤖 Generating AI explanation..."):
                        explanation = generate_ai_explanation(
                            q['Question'], options, correct, ans, question_type, passage_text
                        )
                        st.session_state.explanations[explanation_key] = explanation
               
                if st.session_state.show_explanation:
                    explanation = st.session_state.explanations[explanation_key]
                    st.markdown(f"""
                    <div class="explanation-card">
                        <h3>🤖 AI Explanation</h3>
                        <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 1.5rem;">{explanation}</p>
                    </div>
                    """, unsafe_allow_html=True)
                   
                    # Audio button
                    audio_file_path = f"explanation_{st.session_state.index}_{selected_year}.mp3"
                    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
                    if st.button("🔊 Play Audio", key=f"play_audio_{st.session_state.index}_{selected_year}"):
                        with st.spinner("🎵 Generating audio..."):
                            generated_path = generate_audio_file_openai(explanation, audio_file_path)
                        if generated_path:
                            st.audio(generated_path, format="audio/mp3", autoplay=True)
                    st.markdown('</div>', unsafe_allow_html=True)
               
                # Toggle explanation button
                button_text = "🙈 Hide Explanation" if st.session_state.show_explanation else "🤖 Get AI Explanation"
                st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
                if st.button(button_text, key="toggle_explanation"):
                    st.session_state.show_explanation = not st.session_state.show_explanation
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    # Reset Quiz Button
    st.markdown('<div class="secondary-btn" style="margin-top: 2rem; text-align: center;">', unsafe_allow_html=True)
    if st.button("🔄 Reset Quiz", key="reset_button"):
        st.session_state.year_data[selected_year] = {
            "index": 0,
            "score": 0,
            "submitted": False,
            "attempted": {},
            "show_explanation": False,
            "explanations": {}
        }
       
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.submitted = False
        st.session_state.attempted = {}
        st.session_state.show_explanation = False
        st.session_state.explanations = {}
        save_current_state()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Final Results Summary (when quiz is complete)
    if st.session_state.index == len(df) - 1 and st.session_state.submitted:
        attempted_questions = [k for k, v in st.session_state.attempted.items() if v != "SKIPPED"]
        if len(attempted_questions) == len(df) or len(attempted_questions) >= len(df) * 0.8:  # 80% completion threshold
            final_accuracy = (st.session_state.score / len(attempted_questions)) * 100 if attempted_questions else 0
           
            # Performance evaluation
            if final_accuracy >= 80:
                performance_msg = "🌟 Outstanding! You're ready for WAEC!"
                performance_class = "performance-excellent"
                performance_style = "background: linear-gradient(135deg, #10b981, #059669);"
            elif final_accuracy >= 70:
                performance_msg = "👍 Great work! Keep practicing!"
                performance_class = "performance-good"
                performance_style = "background: linear-gradient(135deg, #3b82f6, #1d4ed8);"
            elif final_accuracy >= 60:
                performance_msg = "📚 Good effort! More practice will help!"
                performance_class = "performance-average"
                performance_style = "background: linear-gradient(135deg, #f59e0b, #d97706);"
            else:
                performance_msg = "💪 Keep studying! You're improving!"
                performance_class = "performance-needs-work"
                performance_style = "background: linear-gradient(135deg, #ef4444, #dc2626);"
           
            st.markdown(f"""
            <div class="final-results">
                <h2>🎯 Quiz Complete!</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{st.session_state.score}</div>
                        <div class="stat-label">Correct Answers</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{len(attempted_questions)}</div>
                        <div class="stat-label">Questions Attempted</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{final_accuracy:.1f}%</div>
                        <div class="stat-label">Accuracy Rate</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{len(df) - len(attempted_questions)}</div>
                        <div class="stat-label">Questions Skipped</div>
                    </div>
                </div>
                <div class="performance-message" style="{performance_style} color: white;">
                    {performance_msg}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Download results option
            results_data = {
                'Question_Number': [],
                'Your_Answer': [],
                'Correct_Answer': [],
                'Result': []
            }
           
            for i in range(len(df)):
                if i in st.session_state.attempted:
                    user_answer = st.session_state.attempted[i]
                    correct_answer = df.iloc[i]["Answer"].strip().upper()
                   
                    results_data['Question_Number'].append(i + 1)
                    results_data['Your_Answer'].append(user_answer)
                    results_data['Correct_Answer'].append(correct_answer)
                    results_data['Result'].append("✅ Correct" if user_answer == correct_answer else "❌ Incorrect")
           
            results_df = pd.DataFrame(results_data)
            csv_data = results_df.to_csv(index=False)
           
            st.download_button(
                label="📥 Download Results",
                data=csv_data,
                file_name=f"waec_english_{selected_year}_results.csv",
                mime="text/csv",
                key="download_results"
            )

except IndexError:
    st.error("❌ Question index out of range. Resetting to first question.")
    st.session_state.index = 0
    st.rerun()

except Exception as e:
    st.error(f"❌ An unexpected error occurred: {str(e)}")
    st.info("Please try refreshing the page or contact support if the problem persists.")

# Close main container
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="app-footer">
    <p>Made with ❤️ for WAEC Success | © 2024 WAEC English Mastery</p>
    <p>💡 Practice consistently and review explanations to master your English skills!</p>
    <p style="font-size: 0.8rem; opacity: 0.7;">
        ✨ Features: AI Explanations • Audio Support • Progress Tracking • Multi-Year Support
    </p>
</div>
""", unsafe_allow_html=True)

# Clean up temporary audio files periodically
import glob
audio_files = glob.glob("explanation_*.mp3")
if len(audio_files) > 20:  # Keep only recent 20 audio files
    for old_file in audio_files[:-20]:
        try:
            os.remove(old_file)
        except:
            pass