# llm_guide_app.py
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import pandas as pd
import re
import os
import random
import requests

# --- App Config ---
st.set_page_config(page_title="LLM Guide for Startups", page_icon="🤖", layout="wide")

# --- Load CSS ---
if os.path.exists("WebAppstyling.css"):
    with open("WebAppstyling.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Hugging Face API Key ---
HUGGINGFACE_API_KEY = st.secrets["HUGGINGFACE_API_KEY"]

# --- Session State Init ---
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
    expanded = st.session_state.get('global_expansion_state', False)
    return st.expander(title, expanded=expanded)

def custom_expander(title):
    expanded = st.session_state.get('global_expansion_state', False)
    return st.expander(title, expanded=expanded)

def display_expand_collapse_controls():
    visible_on_pages = [
        "Home", "Prompt Engineering", "Temperature & Sampling", "Hallucinations",
        "API Cost Optimization", "Ethics & Bias"
    ]
    if page_titles[st.session_state['current_page_index']] in visible_on_pages:
        col1, col2, col3 = st.columns([7, 1, 1])
        with col2:
            if st.button("➕ Expand All", help="Expand all sections"):
                st.session_state['global_expansion_state'] = True
        with col3:
            if st.button("➖ Collapse All", help="Collapse all sections"):
                st.session_state['global_expansion_state'] = False

def show_expand_collapse_buttons():
    display_expand_collapse_controls()

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def store_feedback(entry, path="feedback.csv"):
    new_entry_df = pd.DataFrame([entry])
    if os.path.exists(path):
        existing_df = pd.read_csv(path)
        new_entry_df = pd.concat([existing_df, new_entry_df], ignore_index=True)
    new_entry_df.to_csv(path, index=False)

def get_llm_response(prompt):
    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        payload = {"inputs": prompt, "parameters": {"temperature": 0.7, "max_new_tokens": 200}}
        response = requests.post(
            "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct",
            headers=headers, json=payload
        )
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                return result[0]["generated_text"], None
            else:
                return str(result), None
        else:
            return None, f"❌ HF API Error {response.status_code}: {response.text}"
    except Exception as e:
        return None, f"❌ Exception: {str(e)}"

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
        icons=["house", "pencil", "sliders", "exclamation-circle", "cash-coin", "shield-check",
               "question-circle", "book", "tools", "download", "chat-dots"],
        menu_icon="cast",
        default_index=st.session_state['current_page_index']
    )
    st.session_state['current_page_index'] = page_titles.index(current_page)

# --- Page Logic ---
if current_page == "Home":
    st.markdown("<h1 style='text-align:center;'>Smart Startups. Smart AI.</h1>", unsafe_allow_html=True)
    display_expand_collapse_controls()
    # ... Home content ...

elif current_page == "Prompt Engineering":
    st.title("🧠 Prompt Like a Pro")
    display_expand_collapse_controls()
    # ... Prompt Engineering content ...

elif current_page == "Temperature & Sampling":
    st.title("🎛️ Temperature & Sampling")
    display_expand_collapse_controls()
    # ... Temperature content ...

elif current_page == "API Cost Optimization":
    st.header("💸 Saving Money with LLM APIs")
    display_expand_collapse_controls()
    # ... Cost Optimization content ...

elif current_page == "Ethics & Bias":
    st.header("⚖️ Responsible AI Use for Startups")
    show_expand_collapse_buttons()
    # ... Ethics content ...

elif current_page == "FAQs":
    st.header("❓ Frequently Asked Questions")
    show_expand_collapse_buttons()
    # ... FAQ content ...

elif current_page == "Glossary":
    st.header("📖 Glossary of Common Terms")
    show_expand_collapse_buttons()
    # ... Glossary content ...

elif current_page == "Interactive Use Cases":
    st.header("🧪 AI Use Case Simulator")
    show_expand_collapse_buttons()
    # ... Interactive content ...

elif current_page == "Download Toolkit":
    st.header("📦 Downloadable Toolkit")
    show_expand_collapse_buttons()
    # ... Toolkit content ...

elif current_page == "Feedback":
    st.header("💬 We Value Your Feedback")
    show_expand_collapse_buttons()
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
            "S.No": len(st.session_state['feedback_entries']) + 1,
            "Name": name.strip(),
            "Email": email.strip(),
            "Rating": rating,
            "Feedback": feedback.strip(),
            "Suggested topic": None if suggestion == "None" else suggestion,
            "Attachment name": attachment.name if attachment else None
        }
        st.session_state['feedback_entries'].append(entry)
        store_feedback(entry)
        st.success(f"Thanks {name.strip()} for your feedback!")

    if st.session_state['feedback_entries']:
        if st.checkbox("Show All Feedback"):
            df = pd.DataFrame(st.session_state['feedback_entries'])
            if 'S.No' in df.columns:
                df = df.drop(columns=['S.No'])
            df.index = df.index + 1
            st.dataframe(df, use_container_width=True)

# --- Navigation Buttons ---
nav_prev, _, nav_next = st.columns([2, 6, 2])
with nav_prev:
    if st.session_state['current_page_index'] > 0:
        st.button("⬅️ Previous", on_click=lambda: st.session_state.update({'current_page_index': st.session_state['current_page_index'] - 1}))
with nav_next:
    if st.session_state['current_page_index'] < len(page_titles) - 1:
        st.button("Next ➡️", on_click=lambda: st.session_state.update({'current_page_index': st.session_state['current_page_index'] + 1}))

if st.session_state['current_page_index'] != page_titles.index(current_page):
    st.rerun()

# --- Footer ---
st.markdown("---")
st.caption(f"© 2025 LLM Startup Guide • Last updated {datetime.now().strftime('%Y-%m-%d')}")
