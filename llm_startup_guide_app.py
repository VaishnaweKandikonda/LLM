import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import pandas as pd
import re
import os
import random  # Required for prompt generator

# --- App Config ---
st.set_page_config(page_title="LLM Guide for Startups", page_icon="🤖", layout="wide")

# --- Load CSS ---
if os.path.exists("WebAppstyling.css"):
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
        # Align to top right
        col1, col2, col3 = st.columns([7, 1, 1])
        with col2:
            if st.button("➕ Expand All", help="Expand all sections"):
                st.session_state['global_expansion_state'] = True
        with col3:
            if st.button("➖ Collapse All", help="Collapse all sections"):
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

# --- Pages ---
if current_page == "Home":
    st.markdown("<h1 style='text-align:center;'>Smart Startups. Smart AI.</h1>", unsafe_allow_html=True)
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

elif current_page == "Prompt Engineering":
    st.title("🧠 Prompt Like a Pro")
    display_expand_collapse_controls()

    st.markdown("Choose a sub-topic:")
    st.selectbox("", ["All", "What is a Prompt?", "Best Practices", "Try it Yourself", "Quiz"], label_visibility="collapsed")

    with expander_section("1. What is a Prompt?"):
        st.write("A **prompt** is the instruction you give to an AI. The clearer you are, the better the result.")

    with expander_section("2. Best Practices"):
        st.markdown("- Be Specific\n- Set a Role\n- Define the Output Format")
        st.success("""
        🎯 Example Prompt:\n
        "Act as a SaaS growth marketer. Write a 2-line social media post in a friendly tone promoting our new AI-based customer onboarding tool."
        """)

    with expander_section("3. Vague vs. Clear Prompt Examples"):
        col1, col2 = st.columns(2)
        with col1:
            st.error("❌ Vague Prompt")
            st.markdown("- Describe our app\n- Write something about our new feature")
        with col2:
            st.success("✅ Clear Prompt")
            st.markdown("- Write a 3-sentence product description...\n- Write a 2-sentence feature announcement...")

    with expander_section("4. ✍️ Try it Yourself"):
        user_prompt = st.text_area("Enter your business prompt:")
        if user_prompt:
            st.success(f"“Here’s what a language model might say: {user_prompt.lower()} — designed for modern users.”")

    with expander_section("5. What are you using the prompt for?"):
        use_case = st.radio("", ["Marketing", "Customer Support", "Product", "Sales"], horizontal=True)
        suggestions = {
            "Marketing": "Write a tagline for a social media post promoting our product launch.",
            "Customer Support": "Respond to a refund request in a helpful and polite tone.",
            "Product": "Summarize a product spec in under 50 words.",
            "Sales": "Write a follow-up email to a lead who downloaded our whitepaper."
        }
        st.info(f"💡 Try: '{suggestions[use_case]}'")

    with expander_section("6. 🎲 Prompt Generator"):
        samples = [
            "Write a product update email for a budgeting app used by freelancers.",
            "Draft a refund response message that is friendly and professional.",
            "Create an onboarding message for users who signed up for a beta test.",
            "Write an app store description for a sleep tracking app targeting remote workers."
        ]
        if st.button("🎲 Give me a random prompt"):
            st.write(random.choice(samples))

    with expander_section("7. ✅ Prompt Checklist"):
        st.markdown("- [x] Be specific\n- [x] Set a role\n- [x] Define output format")

    with expander_section("8. 🧠 Test Your Knowledge"):
        q1 = st.radio("1. What makes a good prompt?", [
            "Something short like 'Write something'",
            "Clear instructions with role, format, and topic",
            "Anything, the AI will figure it out"
        ])
        st.success("✅ Correct!") if q1 == "Clear instructions with role, format, and topic" else st.error("❌ Try again.")

        q2 = st.radio("2. Which is a strong ad prompt?", [
            "Write an ad",
            "Write a 2-line ad copy for a wearable fitness tracker targeting new moms in a friendly tone",
            "Make something catchy"
        ])
        st.success("✅ Spot on!") if "fitness tracker" in q2 else st.error("❌ Try again.")

        q3 = st.radio("3. True or False: AI always knows your intent.", ["True", "False"])
        st.success("✅ Correct!") if q3 == "False" else st.error("❌ Incorrect.")

elif current_page == "Feedback":
    st.header("💬 Share Your Feedback")
    display_expand_collapse_controls()

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
            st.dataframe(feedback_df, use_container_width=True)

# --- Page Navigation ---
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
