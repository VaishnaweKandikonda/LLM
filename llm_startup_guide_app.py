import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import pandas as pd
import re
import os
import openai

# --- Page Config ---
st.set_page_config(
    page_title="LLM Guide for Startups",
    page_icon="🤖",
    layout="wide"
)

# --- Load OpenAI API Key ---
openai.api_key = st.secrets["openai"]["api_key"]

# --- Session State Initialization ---
if 'feedback' not in st.session_state:
    if os.path.exists("feedback.csv"):
        st.session_state['feedback'] = pd.read_csv("feedback.csv").to_dict("records")
    else:
        st.session_state['feedback'] = []

if 'page_index' not in st.session_state:
    st.session_state['page_index'] = 0
if 'expand_all' not in st.session_state:
    st.session_state['expand_all'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# --- Helper Functions ---
def custom_expander(label):
    expanded = st.session_state['expand_all'] if st.session_state['expand_all'] is not None else False
    return st.expander(label, expanded=expanded)

def show_expand_collapse_buttons():
    current_page = all_sections[st.session_state['page_index']]
    target_pages = [
        "Home", "Prompt Engineering", "Temperature & Sampling", "Hallucinations",
        "API Cost Optimization", "Ethics & Bias"
    ]
    if current_page in target_pages:
        col1, col2, col3 = st.columns([6, 1, 1])
        with col2:
            if st.button("➕", help="Expand All Sections"):
                st.session_state['expand_all'] = True
        with col3:
            if st.button("➖", help="Collapse All Sections"):
                st.session_state['expand_all'] = False

def save_feedback_to_csv(entry, path="feedback.csv"):
    df = pd.DataFrame([entry])
    if os.path.exists(path):
        existing = pd.read_csv(path)
        df = pd.concat([existing, df], ignore_index=True)
    df.to_csv(path, index=False)

def is_valid_email(email_str):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email_str)

# --- Sidebar Menu ---
all_sections = [
    "Home", "Prompt Engineering", "Temperature & Sampling", "Hallucinations",
    "API Cost Optimization", "Ethics & Bias", "FAQs", "Glossary",
    "Interactive Use Cases", "Download Toolkit", "Feedback"
]

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=all_sections,
        icons=[
            "house", "pencil", "sliders", "exclamation-circle", "cash-coin", "shield-check",
            "question-circle", "book", "tools", "download", "chat-dots"
        ],
        menu_icon="cast",
        default_index=st.session_state['page_index']
    )
    st.session_state['page_index'] = all_sections.index(selected)

# --- HOME PAGE ---
if selected == "Home":
    st.markdown("""
        <h1 style='text-align: center; font-size: 3em; color: #333;'>Smart Startups. Smart AI.</h1>
        <style>
        .stButton>button {
            transition: 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #00bcd4 !important;
            color: white !important;
            transform: scale(1.05);
        }
        .custom-card {
            padding: 1em;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            background-color: white;
            transition: 0.3s ease;
            margin-bottom: 1rem;
        }
        .custom-card:hover {
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            transform: scale(1.01);
        }
        @media screen and (max-width: 768px) {
            h1 {
                font-size: 2em !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    show_expand_collapse_buttons()

    for title, content in {
        "🤖 What are Language Models?": "Language models are AI tools trained to understand and generate human-like text. Tools like ChatGPT, Claude, and Gemini are based on LLMs.",
        "💡 Why Should Startups Care?": """
            LLMs can help you:
            - Write product descriptions and marketing copy
            - Automate customer support and FAQ generation
            - Draft emails, blogs, and pitch decks
            - Prototype conversational agents and tools
        """,
        "🚀 What You’ll Learn in This Guide": """
            - How to write better prompts
            - How temperature affects creativity
            - How to spot and avoid hallucinations
            - How to save on API costs
            - How to use LLMs ethically
        """
    }.items():
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        with custom_expander(title):
            st.markdown(content)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Chatbot ---
    st.markdown("---")
    st.subheader("🤖 Ask Our AI Assistant")

    user_input = st.chat_input("Ask something about LLMs or startups...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for startup founders using AI."}
                    ] + st.session_state.chat_history
                )
                ai_reply = response.choices[0].message["content"]
                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
            except Exception as e:
                ai_reply = f"⚠️ Error: {e}"
                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

    if st.button("Reset Chat"):
        st.session_state.chat_history = []
        st.experimental_rerun()

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- Placeholder for other pages ---
elif selected == "Feedback":
    st.header("💬 We Value Your Feedback")
    show_expand_collapse_buttons()

    st.markdown("Please share your thoughts on this guide.")

    name = st.text_input("Your name *")
    email = st.text_input("Your email (optional)")
    rating = st.slider("How helpful was this guide?", 1, 5, 3)
    feedback = st.text_area("Your thoughts (optional)")
    suggestion = st.selectbox("What would you like to see next?", ["None", "LLM APIs", "Customer Support", "Tool Comparisons", "No-code Prototyping"])
    attachment = st.file_uploader("📎 Attach a file (optional)", type=["png", "jpg", "pdf", "txt", "docx"])

    required_filled = bool(name.strip())
    email_valid = True if not email.strip() else is_valid_email(email.strip())
    form_valid = required_filled and email_valid

    if st.button("Submit Feedback", disabled=not form_valid):
        entry = {
            "S.No": len(st.session_state['feedback']) + 1,
            "Name": name.strip(),
            "Email": email.strip(),
            "Rating": rating,
            "Feedback": feedback.strip(),
            "Suggested topic": None if suggestion == "None" else suggestion,
            "Attachment name": attachment.name if attachment else None
        }
        st.session_state['feedback'].append(entry)
        save_feedback_to_csv(entry)
        st.success(f"Thanks {name.strip()} for your feedback!")

    if st.session_state['feedback']:
        if st.checkbox("Show All Feedback"):
            df = pd.DataFrame(st.session_state['feedback'])
            st.dataframe(df.reset_index(drop=True), use_container_width=True)

# --- Navigation Buttons ---
st.markdown("---")
nav_col1, nav_col2, nav_col3 = st.columns([2, 4, 2])
with nav_col1:
    if st.session_state['page_index'] > 0:
        if st.button("⬅️ Previous"):
            st.session_state['page_index'] -= 1
            st.rerun()
with nav_col3:
    if st.session_state['page_index'] < len(all_sections) - 1:
        if st.button("Next ➡️"):
            st.session_state['page_index'] += 1
            st.rerun()

# --- Footer ---
st.markdown("---")
st.caption(f"© 2025 LLM Startup Guide – Last updated {datetime.now().strftime('%Y-%m-%d')}")
