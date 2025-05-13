import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import pandas as pd
import re
import os

# --- App Config ---
st.set_page_config(page_title="LLM Guide for Startups", page_icon="🤖", layout="wide")

# --- Load CSS ---
with open("WebAppstyling.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Session State ---
if 'feedback_entries' not in st.session_state:
    if os.path.exists("feedback.csv"):
        st.session_state['feedback_entries'] = pd.read_csv("feedback.csv").to_dict("records")
    else:
        st.session_state['feedback_entries'] = []

if 'current_page_index' not in st.session_state:
    st.session_state['current_page_index'] = 0
if 'global_expansion_state' not in st.session_state:
    st.session_state['global_expansion_state'] = None

# --- Utility Functions ---
def expander_section(title):
    expanded = st.session_state['global_expansion_state'] if st.session_state['global_expansion_state'] is not None else False
    return st.expander(title, expanded=expanded)

def display_expand_collapse_controls():
    visible_on_pages = [
        "Home", "Prompt Engineering", "Temperature & Sampling", "Hallucinations",
        "API Cost Optimization", "Ethics & Bias"
    ]
    if page_titles[st.session_state['current_page_index']] in visible_on_pages:
        _, col_expand, col_collapse = st.columns([6, 1, 1])
        with col_expand:
            if st.button("➕ Expand All", help="Open all content sections"):
                st.session_state['global_expansion_state'] = True
        with col_collapse:
            if st.button("➖ Collapse All", help="Close all content sections"):
                st.session_state['global_expansion_state'] = False

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def store_feedback(entry, path="feedback.csv"):
    new_entry_df = pd.DataFrame([entry])
    if os.path.exists(path):
        existing_df = pd.read_csv(path)
        new_entry_df = pd.concat([existing_df, new_entry_df], ignore_index=True)
    new_entry_df.to_csv(path, index=False)

# --- Sidebar Navigation ---
page_titles = [
    "Home", "Prompt Engineering", "Temperature & Sampling", "Hallucinations",
    "API Cost Optimization", "Ethics & Bias", "FAQs", "Glossary",
    "Interactive Use Cases", "Download Toolkit", "Feedback"
]

with st.sidebar:
    current_page = option_menu(
        menu_title="📘 Guide Sections",
        options=page_titles,
        icons=[
            "house", "pencil", "sliders", "exclamation-circle", "cash-coin", "shield-check",
            "question-circle", "book", "tools", "download", "chat-dots"
        ],
        menu_icon="cast",
        default_index=st.session_state['current_page_index']
    )
    st.session_state['current_page_index'] = page_titles.index(current_page)

# --- Home Page ---
if current_page == "Home":
    st.markdown("<h1>Smart Startups. Smart AI.</h1>", unsafe_allow_html=True)
    display_expand_collapse_controls()

    home_sections = {
        "🤖 Introduction to Large Language Models": (
            "Large Language Models (LLMs) are advanced AI systems trained to understand and generate human-like text. "
            "Popular platforms like ChatGPT, Claude, and Gemini use LLMs to assist users with content generation, problem-solving, and more."
        ),
        "💡 Why LLMs Matter for Startups": (
            "- Automate customer support and FAQs\n"
            "- Generate pitch decks, emails, blogs, and product content\n"
            "- Build intelligent prototypes and chatbots\n"
            "- Accelerate idea validation and MVP development"
        ),
        "✅ Let's Get Started!": (
            "Use the left menu to explore sections packed with insights, use cases, and practical tools to build smarter with AI."
        ),
        "🔍 Best Practices & Ethics": (
            "- Learn prompt design for better results\n"
            "- Understand model temperature and creativity\n"
            "- Avoid AI-generated misinformation\n"
            "- Optimize API costs\n"
            "- Navigate bias and fairness responsibly"
        ),
        "👥 Who Should Use This Guide": (
            "- Startup founders exploring AI\n"
            "- Developers and PMs integrating LLMs\n"
            "- Investors evaluating AI strategies\n"
            "- Anyone curious about AI in startups"
        )
    }

    for title, content in home_sections.items():
        with expander_section(title):
            st.markdown(content)

# --- Feedback Page ---
elif current_page == "Feedback":
    st.header("💬 Share Your Feedback")
    display_expand_collapse_controls()
    st.markdown("We’d love to hear your thoughts and suggestions to improve this guide.")

    user_name = st.text_input("Your Name *")
    user_email = st.text_input("Email (Optional)")
    usefulness_rating = st.slider("How useful was this guide?", 1, 5, 3)
    user_comment = st.text_area("Your Thoughts (Optional)")
    topic_suggestion = st.selectbox("What topic would you like us to cover next?", [
        "None", "LLM APIs", "Customer Support Automation", "Tool Comparisons", "No-code AI Prototyping"
    ])
    uploaded_file = st.file_uploader("📎 Upload a file (Optional)", type=["png", "jpg", "pdf", "txt", "docx"])

    is_name_valid = bool(user_name.strip())
    is_email_valid = True if not user_email.strip() else is_valid_email(user_email.strip())
    form_ready = is_name_valid and is_email_valid

    if not is_name_valid:
        st.warning("Please enter your name.")
    elif not is_email_valid:
        st.warning("Email format appears invalid.")

    if st.button("Submit Feedback", disabled=not form_ready):
        feedback_entry = {
            "Entry No": len(st.session_state['feedback_entries']) + 1,
            "Name": user_name.strip(),
            "Email": user_email.strip(),
            "Rating": usefulness_rating,
            "Feedback": user_comment.strip(),
            "Suggested Topic": None if topic_suggestion == "None" else topic_suggestion,
            "Uploaded File": uploaded_file.name if uploaded_file else None
        }
        st.session_state['feedback_entries'].append(feedback_entry)
        store_feedback(feedback_entry)
        st.success(f"Thanks, {user_name.strip()}! Your feedback has been submitted.")

    if st.session_state['feedback_entries']:
        if st.checkbox("📂 View Submitted Feedback"):
            feedback_df = pd.DataFrame(st.session_state['feedback_entries'])
            st.dataframe(feedback_df.reset_index(drop=True), use_container_width=True)

# --- Page Navigation ---
st.markdown("---")
nav_prev, _, nav_next = st.columns([2, 6, 2])
with nav_prev:
    if st.session_state['current_page_index'] > 0:
        if st.button("⬅️ Previous"):
            st.session_state['current_page_index'] -= 1
            st.rerun()
with nav_next:
    if st.session_state['current_page_index'] < len(page_titles) - 1:
        if st.button("Next ➡️"):
            st.session_state['current_page_index'] += 1
            st.rerun()

# --- Footer ---
st.markdown("---")
st.caption(f"© 2025 LLM Startup Guide • Last updated {datetime.now().strftime('%Y-%m-%d')}")
