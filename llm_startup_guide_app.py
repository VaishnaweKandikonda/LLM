import streamlit as st
from streamlit-option-menu import option_menu
from datetime import datetime
import pandas as pd
import pyttsx3
import threading

# Page Configuration
st.set_page_config(
    page_title="LLM Guide for Startups",
    page_icon="🤖",
    layout="wide"
)

# Initialize Text-to-Speech engine
tts_engine = pyttsx3.init()

def speak_text(text):
    def run_speech():
        tts_engine.say(text)
        tts_engine.runAndWait()
    threading.Thread(target=run_speech).start()

# Initialize session state
if 'feedback_data' not in st.session_state:
    st.session_state['feedback_data'] = []
if 'current_section_index' not in st.session_state:
    st.session_state['current_section_index'] = 0

# Navigation sections
sections = [
    "Home", "Prompt Engineering", "Temperature & Sampling", "Hallucinations",
    "API Cost Optimization", "Ethics & Bias", "FAQs", "Glossary",
    "Interactive Use Cases", "Download Toolkit", "Feedback"
]

# Sidebar Navigation
with st.sidebar:
    selected_section = option_menu(
        menu_title="Main Menu",
        options=sections,
        icons=[
            "house", "pencil", "sliders", "exclamation-circle", "cash-coin", "shield-check",
            "question-circle", "book", "tools", "download", "chat-dots"
        ],
        menu_icon="cast",
        default_index=st.session_state['current_section_index']
    )
    st.session_state['current_section_index'] = sections.index(selected_section)

# Read-aloud functionality
def speak_button(text_content):
    if st.button("🔊 Read Aloud"):
        speak_text(text_content)

# Section Routing
if selected_section == "Home":
    st.title("Smart Startups, Smarter AI")
    intro_text = (
        "Welcome, founders and entrepreneurs! This guide is designed to help you understand and use "
        "large language models effectively, responsibly, and efficiently in your startup."
    )
    st.markdown(intro_text)
    speak_button(intro_text)

    with st.expander("🤖 What are Language Models?"):
        st.markdown("Language models are AI tools trained to understand and generate human-like text. Tools like ChatGPT, Claude, and Gemini are based on LLMs.")

    with st.expander("💡 Why Should Startups Care?"):
        st.markdown("""
        LLMs can help you:
        - Write product descriptions and marketing copy
        - Automate customer support and FAQ generation
        - Draft emails, blogs, and pitch decks
        - Prototype conversational agents and tools

        But they also come with risks — like false information (hallucinations), cost inefficiencies, and ethical concerns.
        """)

    with st.expander("🚀 What You’ll Learn in This Guide"):
        st.markdown("""
        - How to write better prompts
        - How temperature affects creativity
        - How to spot and avoid hallucinations
        - How to save on API costs
        - How to use LLMs ethically

        Use the **menu on the left** to explore each topic.
        """)

# Additional sections handled in original app...
# You can append the rest of the logic from your original script here in the same format.

# Navigation Controls
st.markdown("---")
nav_col1, _, nav_col2 = st.columns([2, 4, 2])
with nav_col1:
    if st.session_state['current_section_index'] > 0:
        if st.button("⬅️ Previous"):
            st.session_state['current_section_index'] -= 1
            st.rerun()
with nav_col2:
    if st.session_state['current_section_index'] < len(sections) - 1:
        if st.button("Next ➡️"):
            st.session_state['current_section_index'] += 1
            st.rerun()

# Footer
st.markdown("---")
st.caption(f"© 2025 LLM Startup Guide – Last updated {datetime.now().strftime('%Y-%m-%d')}")
