import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import pandas as pd
import re
import os

# Page Config
st.set_page_config(
    page_title="LLM Guide for Startups",
    page_icon="🤖",
    layout="wide"
)

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

# --- Helper Functions ---
def custom_expander(label):
    expanded = st.session_state['expand_all'] if st.session_state['expand_all'] is not None else False
    return st.expander(label, expanded=expanded)

def show_expand_collapse_buttons():
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("➕ Expand All"):
            st.session_state['expand_all'] = True
    with col2:
        if st.button("➖ Collapse All"):
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

# --- Section Routing ---
if selected == "Home":
    st.title("Smart Startups, Smarter AI")
    show_expand_collapse_buttons()
    st.markdown("Welcome, founders and entrepreneurs! This guide is designed to help you understand and use large language models effectively, responsibly, and efficiently in your startup.")

    with custom_expander("🤖 What are Language Models?"):
        st.markdown("Language models are AI tools trained to understand and generate human-like text. Tools like ChatGPT, Claude, and Gemini are based on LLMs.")

    with custom_expander("💡 Why Should Startups Care?"):
        st.markdown("""
        LLMs can help you:
        - Write product descriptions and marketing copy
        - Automate customer support and FAQ generation
        - Draft emails, blogs, and pitch decks
        - Prototype conversational agents and tools
        """)

    with custom_expander("🚀 What You’ll Learn in This Guide"):
        st.markdown("""
        - How to write better prompts
        - How temperature affects creativity
        - How to spot and avoid hallucinations
        - How to save on API costs
        - How to use LLMs ethically
        """)

elif selected == "Prompt Engineering":
    st.header("🧠 Prompt Like a Pro")
    show_expand_collapse_buttons()
    sub = st.selectbox("Choose a sub-topic:", ["All", "What is a Prompt?", "Best Practices", "Try It Yourself"])

    if sub in ["All", "What is a Prompt?"]:
        with custom_expander("🔍 What is a Prompt?"):
            st.markdown("A **prompt** is the text you give to an AI model to guide its response. The clearer your prompt, the better the output.")

    if sub in ["All", "Best Practices"]:
        with custom_expander("🛠️ Best Practices"):
            st.markdown("""
            - Be **specific**
            - Set a **role**
            - Define the **output format**
            """)

    if sub in ["All", "Try It Yourself"]:
        with custom_expander("✍️ Try it Yourself"):
            user_prompt = st.text_area("Enter a prompt you'd use for your business:", "Write a catchy product description for a new app that tracks sleep patterns.")
            if user_prompt:
                st.markdown(f"_Example result:_\n\n> \"{user_prompt.replace('Write a', 'Introducing our new tool that helps you')}\"")

elif selected == "Temperature & Sampling":
    st.header("🎛️ Controlling AI Creativity")
    show_expand_collapse_buttons()
    sub = st.selectbox("Choose a sub-topic:", ["All", "What is Temperature?", "Live Example"])

    if sub in ["All", "What is Temperature?"]:
        with custom_expander("🔥 What is Temperature?"):
            st.markdown("""
            Temperature controls how **random** or **creative** the AI’s response will be:
            - `0.0` = Very precise
            - `0.7` = Balanced
            - `1.0` = Very creative
            """)

    if sub in ["All", "Live Example"]:
        with custom_expander("🤖 Try adjusting the temperature"):
            temp = st.slider("Choose a temperature:", 0.0, 1.0, 0.7, 0.1)
            sample_prompt = "Describe a smart water bottle in one sentence."
            if temp < 0.3:
                result = "A smart water bottle that reminds you to drink water every hour."
            elif temp < 0.7:
                result = "A smart water bottle that tracks your hydration and connects to your phone."
            else:
                result = "Imagine a sleek bottle that whispers hydration tips and syncs with your wellness dreams."
            st.write(f"**Prompt:** {sample_prompt}")
            st.success(f"Output: {result}")

elif selected == "Hallucinations":
    st.header("🚨 Avoiding AI Hallucinations")
    show_expand_collapse_buttons()

    with custom_expander("🧠 Why It Happens"):
        st.markdown("LLMs predict text based on patterns in data. They do not \"know\" truth.")

    with custom_expander("🚫 Example"):
        st.markdown("""
        **Prompt:** "What’s the latest GDPR certification for startups?"  
        **LLM Output:** "The 2024 GDPR-AI Gold Standard certification…" ❌ _(this does not exist)_
        """)

    with custom_expander("✅ Best Practices"):
        st.markdown("""
        - Cross-check AI outputs
        - Don’t use LLMs for critical info
        - Add human review
        """)

elif selected == "API Cost Optimization":
    st.header("💸 Saving Money with LLM APIs")
    show_expand_collapse_buttons()

    with custom_expander("📉 Why It Matters"):
        st.markdown("LLM API calls cost money. Reduce usage where possible.")

    with custom_expander("💰 Strategies to Reduce Cost"):
        st.markdown("""
        - Use GPT-3.5 when possible
        - Keep prompts short
        - Batch tasks
        - Use caching
        """)

    with custom_expander("📊 Cost Example"):
        st.markdown("""
        - 100 GPT-4 calls = ~$3  
        - 100 GPT-3.5 calls = ~$0.20
        """)

elif selected == "Ethics & Bias":
    st.header("⚖️ Responsible AI Use for Startups")
    show_expand_collapse_buttons()

    with custom_expander("⚠️ What’s the Risk?"):
        st.markdown("LLMs can reflect or amplify **biases** in their training data.")

    with custom_expander("🧪 Example"):
        st.markdown("""
        **Prompt:** "Describe a CEO."  
        **Output:** "He is a confident leader..." ❌ _(gender bias)_
        """)

    with custom_expander("🛡 How to Mitigate"):
        st.markdown("""
        - Use inclusive language
        - Check outputs for bias
        - Document usage policy
        """)

elif selected == "FAQs":
    st.header("❓ Frequently Asked Questions")
    show_expand_collapse_buttons()

    with custom_expander("What is a language model?"):
        st.write("An AI trained to understand/generate human language.")
    with custom_expander("What is a token?"):
        st.write("A small unit of text. Token count affects API cost.")
    with custom_expander("Can I trust the output?"):
        st.write("Not always. Use human verification.")
    with custom_expander("Is GPT-3.5 enough for my startup?"):
        st.write("Often, yes! It’s cheaper and works for most tasks.")

elif selected == "Glossary":
    st.header("📖 Glossary of Common Terms")
    show_expand_collapse_buttons()
    terms = {
        "LLM": "Large Language Model",
        "Token": "Unit of input text processed by the model",
        "Prompt": "Instruction given to an AI",
        "Temperature": "Controls output creativity",
        "Hallucination": "False output from LLM",
        "Bias": "Systemic unfairness in output"
    }
    for term, definition in terms.items():
        st.markdown(f"**{term}** — {definition}")

elif selected == "Interactive Use Cases":
    st.header("🧪 AI Use Case Simulator")
    show_expand_collapse_buttons()
    use_case = st.selectbox("Choose a scenario:", ["Product Description", "Customer Support Reply", "Marketing Email"])

    if use_case == "Product Description":
        product = st.text_input("Describe your product:", "Eco-friendly water bottle with temperature sensor")
        if product:
            st.success(f"Meet your new hydration hero – {product}.")

    elif use_case == "Customer Support Reply":
        issue = st.text_area("Enter the customer issue:", "The app is not tracking my sleep correctly.")
        if issue:
            st.success(f"Response: Sorry to hear that! Try reinstalling. We're on it: '{issue}'.")

    elif use_case == "Marketing Email":
        offer = st.text_input("What's your campaign about?", "10% off all subscriptions this month")
        if offer:
            st.success(f"Email: Unlock your {offer}! Tools that work for you. Limited time!")

elif selected == "Download Toolkit":
    st.header("📦 Downloadable Toolkit")
    show_expand_collapse_buttons()
    toolkit = """LLM Guide for Startups - Toolkit\n\nPROMPTING: Be specific, assign a role, define format\nTEMPERATURE: 0 = factual, 1 = creative\nHALLUCINATIONS: Always verify info\nCOST: Use GPT-3.5, keep prompts short\nETHICS: Use inclusive language, test bias"""
    st.download_button("📥 Download Toolkit as TXT", data=toolkit, file_name="llm_startup_toolkit.txt")

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
