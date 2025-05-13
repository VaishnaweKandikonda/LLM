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

def get_llm_response(prompt):
    import streamlit as st
    import requests

    HUGGINGFACE_API_KEY = st.secrets["HUGGINGFACE_API_KEY"]

    try:
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
        }

        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": 0.7,
                "max_new_tokens": 200
            }
        }

        response = requests.post(
            "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                return result[0]["generated_text"], None
            else:
                return str(result), None  # fallback
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

# --- Prompt Engineering Page ---
elif current_page == "Prompt Engineering":
    st.title("🧠 Prompt Like a Pro")
    display_expand_collapse_controls()

    st.markdown("### Choose a sub-topic to explore:")
    subtopic = st.selectbox(
        "Select a topic:",
        ["All", "What is a Prompt?", "Best Practices", "Vague vs. Clear Examples",
         "Try it Yourself", "Prompt Use Cases", "Prompt Generator", "Prompt Checklist", "Quiz"]
    )

    if subtopic in ("All", "What is a Prompt?"):
        with expander_section("1. What is a Prompt?"):
            st.write("""
            A **prompt** is the instruction you give to an AI model. Think of it like a creative brief — 
            the clearer you are, the better the output.
            """)

    if subtopic in ("All", "Best Practices"):
        with expander_section("2. Best Practices"):
            st.markdown("- Be Specific\n- Set a Role\n- Define Output Format")
            st.success("""
            🎯 Example Prompt:\n
            \"Act as a SaaS growth marketer. Write a 2-line social media post in a friendly tone promoting our new AI-based customer onboarding tool.\"
            """)

    if subtopic in ("All", "Vague vs. Clear Examples"):
        with expander_section("3. Vague vs. Clear Prompt Examples"):
            col1, col2 = st.columns(2)
            with col1:
                st.error("❌ Vague Prompt")
                st.markdown("- Describe our app\n- Write something about our new feature")
            with col2:
                st.success("✅ Clear Prompt")
                st.markdown("- Write a 3-sentence product description...\n- Write a 2-sentence announcement...")

    if subtopic in ("All", "Try it Yourself"):
        with expander_section("4. ✍️ Try it Yourself"):
            st.markdown("Write a real prompt you'd like to test. We'll generate a response using FLAN-T5.")
            user_prompt = st.text_area("Enter your business prompt:")

            if user_prompt:
                with st.spinner("Generating response..."):
                    response, error = get_llm_response(user_prompt)

                    if response:
                        st.success(response)
                    else:
                        st.error(error)

    if subtopic in ("All", "Prompt Use Cases"):
        with expander_section("5. What are you using the prompt for?"):
            use_case = st.radio("", ["Marketing", "Customer Support", "Product", "Sales"], horizontal=True)
            suggestions = {
                "Marketing": "Write a tagline for a social media post promoting our product launch.",
                "Customer Support": "Respond to a refund request in a helpful and polite tone.",
                "Product": "Summarize a product spec in under 50 words.",
                "Sales": "Write a follow-up email to a lead who downloaded our whitepaper."
            }
            st.info(f"💡 Try: '{suggestions[use_case]}'")

    if subtopic in ("All", "Prompt Generator"):
        with expander_section("6. 🎲 Prompt Generator"):
            samples = [
                "Write a product update email for a budgeting app.",
                "Draft a refund message that is professional.",
                "Create an onboarding message for beta users.",
                "Write an app store description for a sleep tracking app."
            ]
            if st.button("🎲 Give me a random prompt"):
                st.write(random.choice(samples))

    if subtopic in ("All", "Prompt Checklist"):
        with expander_section("7. ✅ Prompt Checklist"):
            st.markdown("- [x] Be specific\n- [x] Set a role\n- [x] Define output format")

    if subtopic in ("All", "Quiz"):
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
elif current_page == "Temperature & Sampling":
    st.title("🎛️ Temperature & Sampling")
    display_expand_collapse_controls()

    with expander_section("🔥 What is Temperature in Language Models?"):
        st.write("""
        **Temperature** controls how predictable or creative the AI's output is.

        It ranges from **0.0 to 1.0**:
        - A **low temperature** (e.g., 0.1) makes the model **precise, reliable, and factual**.
        - A **high temperature** (e.g., 0.9) makes it **creative, surprising, and more risky**.

        Think of it like this:
        > 🔧 0.1 = robotic, safe replies  
        > 🎨 0.9 = playful, unexpected ideas
        """)
        st.info("💡 Tip: For investor summaries or product specs → use low temp. For brainstorming ideas or marketing slogans → use high temp.")

    with expander_section("🎯 Adjust the Temperature and See the Difference"):
        temperature = st.slider("Select Temperature Level", 0.1, 1.0, 0.7)
        if temperature < 0.3:
            st.success("🧊 Low Temperature (Factual & Consistent)")
            st.markdown("Example: “Our app helps freelancers manage budgets. It's secure and simple.”")
        elif temperature < 0.7:
            st.info("⚖️ Medium Temperature (Balanced)")
            st.markdown("Example: “Meet the financial sidekick for freelancers — smart, helpful, and always on call.”")
        else:
            st.warning("🔥 High Temperature (Creative & Risky)")
            st.markdown("Example: “Money? Managed. Chaos? Cancelled. Our app is your financial freedom button.”")

    with expander_section("📊 Temperature Summary Table"):
        st.markdown("""
        | Temperature | Behavior                  | Best For                      |
        |-------------|---------------------------|-------------------------------|
        | 0.1 - 0.3   | Factual, focused, safe    | Reports, investor decks       |
        | 0.4 - 0.7   | Balanced, conversational  | Product copy, onboarding flows|
        | 0.8 - 1.0   | Creative, surprising      | Brainstorms, social content   |
        """)

    with expander_section("🎲 What Is Sampling in LLMs?"):
        st.write("""
        **Sampling** is how the model decides **which word to say next**. It picks from a range of likely options, not just the top one.

        Two techniques:
        - **Top-k sampling**: From top k most likely next words
        - **Top-p sampling (nucleus sampling)**: From smallest group of words with probability above p

        This helps avoid repetition and create variation — useful for startups generating product copy, blog posts, or email variations.
        """)

    with expander_section("🧠 Match Temperature to a Task"):
        use_case = st.radio("Select your use case:", 
                            ["Summarizing a feature list", "Generating Instagram ad copy", "Writing a refund response email"])
        if use_case == "Summarizing a feature list":
            st.success("✅ Best with: Low Temperature (0.1 - 0.3)")
        elif use_case == "Generating Instagram ad copy":
            st.warning("🔥 Best with: High Temperature (0.8 - 1.0)")
        elif use_case == "Writing a refund response email":
            st.info("⚖️ Best with: Medium Temperature (0.4 - 0.6)")

    st.markdown("💬 Adjusting temperature = fine-tuning your **startup's voice**: From steady and formal to bold and creative.")
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
            if 'S.No' in df.columns:
                df = df.drop(columns=['S.No'])
            df.index = df.index + 1  # Show index starting from 1
            st.dataframe(df, use_container_width=True)

# --- Navigation Buttons ---
st.markdown("---")
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
