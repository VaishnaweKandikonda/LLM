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
            
# --- Prompt Page ---#
elif current_page == "Prompt Engineering":
    st.title("🧠 Prompt Like a Pro")
    display_expand_collapse_controls()

    st.markdown("Choose a sub-topic:")
    st.selectbox("", ["All", "What is a Prompt?", "Best Practices", "Try it Yourself", "Quiz"], label_visibility="collapsed")

    with expander_section("1. What is a Prompt?"):
        st.write("""
        A **prompt** is the input or instruction you give to an AI model. Think of it like a creative brief — 
        the clearer you are, the better the output. Good prompts tell the AI who it’s writing for, what format to use, and what tone to adopt.
        """)
        st.info("💡 **Pro Tip:** Great AI output starts with great input. Treat your prompt like a business brief.")

    with expander_section("2. Best Practices"):
        st.markdown("""
        - 🧠 **Be Specific**  
        - 🧑‍💼 **Set a Role**  
        - 📝 **Define the Output Format**  
        """)
        st.success("""
        🎯 Example Prompt:
        "Act as a SaaS growth marketer. Write a 2-line social media post in a friendly tone promoting our new AI-based customer onboarding tool."

        ✔️ Specific? → Yes  
        ✔️ Role? → SaaS growth marketer  
        ✔️ Format? → 2-line post, friendly tone
        """)

    with expander_section("3. Vague vs. Clear Prompt Examples"):
        col1, col2 = st.columns(2)
        with col1:
            st.error("❌ Vague Prompt")
            st.markdown("""
            - "Describe our app."
            - "Write something about our new feature."
            """)
        with col2:
            st.success("✅ Clear Prompt")
            st.markdown("""
            - "Write a 3-sentence product description for a budgeting app that helps freelancers track income and expenses. Use a friendly and reassuring tone."
            - "Act as a product marketer. Write a 2-sentence feature announcement for a smart scheduling tool aimed at remote teams."
            """)

    with expander_section("4. ✍️ Try it Yourself"):
        user_prompt = st.text_area("Enter a prompt you'd use for your business:", "Write a catchy product description for a new app that tracks sleep patterns.")
        if user_prompt:
            st.markdown("**Example result:**")
            st.success(f"“Here’s what a language model might say: {user_prompt.lower()} — designed for modern users.”")

    with expander_section("5. What are you using the prompt for?"):
        use_case = st.radio("", ["Marketing", "Customer Support", "Product", "Sales"], horizontal=True)
        if use_case == "Marketing":
            st.info("💡 Try: 'Write a tagline for a social media post promoting our product launch.'")
        elif use_case == "Customer Support":
            st.info("💡 Try: 'Respond to a refund request in a helpful and polite tone.'")
        elif use_case == "Product":
            st.info("💡 Try: 'Summarize a product spec in under 50 words.'")
        elif use_case == "Sales":
            st.info("💡 Try: 'Write a follow-up email to a lead who downloaded our whitepaper.'")

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
        st.markdown("""
        - [x] Be specific  
        - [x] Set a role  
        - [x] Define the output format  
        - [x] Focus on one task  
        """)
        st.warning("⚠️ Don’t rely on generic prompts. Avoid commands like 'Write something for me.'")

    with expander_section("8. 🧠 Test Your Knowledge"):
        # Question 1
        st.markdown("**1. What makes a good prompt for a business use case?**")
        q1 = st.radio("Select one:", [
            "Something short like 'Write something'",
            "Clear instructions with role, format, and topic",
            "Anything, the AI will figure it out"
        ], key="q1")

        if q1:
            if q1 == "Clear instructions with role, format, and topic":
                st.success("✅ Correct! Clear and specific prompts lead to better results.")
            else:
                st.error("❌ Not quite. Vague or unclear prompts lead to weak responses.")

        # Question 2
        st.markdown("**2. Which of these is a strong prompt for generating ad copy?**")
        q2 = st.radio("Select one:", [
            "Write an ad",
            "Write a 2-line ad copy for a wearable fitness tracker targeting new moms in a friendly tone",
            "Make something catchy"
        ], key="q2")

        if q2:
            if q2 == "Write a 2-line ad copy for a wearable fitness tracker targeting new moms in a friendly tone":
                st.success("✅ Spot on! This gives the AI exactly what it needs to write well.")
            else:
                st.error("❌ Try again. Strong prompts are specific about audience, format, and tone.")

        # Question 3
        st.markdown("**3. True or False: ChatGPT always knows exactly what you mean.**")
        q3 = st.radio("Choose one:", ["True", "False"], key="q3")

        if q3:
            if q3 == "False":
                st.success("✅ Correct. ChatGPT follows your prompt exactly — not your intent.")
            else:
                st.error("❌ Incorrect. AI can’t guess what you meant if the prompt is vague.")

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
