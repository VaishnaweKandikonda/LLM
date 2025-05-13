import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import pandas as pd
import re

# Page Config
st.set_page_config(
    page_title="LLM Guide for Startups",
    page_icon="🤖",
    layout="wide"
)

# --- Session State Initialization ---
if 'feedback' not in st.session_state:
    st.session_state['feedback'] = []
if 'page_index' not in st.session_state:
    st.session_state['page_index'] = 0
if 'expand_all' not in st.session_state:
    st.session_state['expand_all'] = None  # Controls expand/collapse of expanders

# --- Helper Function for Expanders ---
def custom_expander(label):
    expanded = st.session_state['expand_all'] if st.session_state['expand_all'] is not None else False
    return st.expander(label, expanded=expanded)

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

    st.markdown("**🧭 Quick View Options**")
    if st.button("➕ Expand All"):
        st.session_state['expand_all'] = True
    if st.button("➖ Collapse All"):
        st.session_state['expand_all'] = False

# --- Section Routing ---
if selected == "Home":
    st.title("Smart Startups, Smarter AI")
    intro = "Welcome, founders and entrepreneurs! This guide is designed to help you understand and use large language models effectively, responsibly, and efficiently in your startup."
    st.markdown(intro)

    with custom_expander("🤖 What are Language Models?"):
        st.markdown("Language models are AI tools trained to understand and generate human-like text. Tools like ChatGPT, Claude, and Gemini are based on LLMs.")

    with custom_expander("💡 Why Should Startups Care?"):
        st.markdown("""
        LLMs can help you:
        - Write product descriptions and marketing copy
        - Automate customer support and FAQ generation
        - Draft emails, blogs, and pitch decks
        - Prototype conversational agents and tools

        But they also come with risks — like false information (hallucinations), cost inefficiencies, and ethical concerns.
        """)

    with custom_expander("🚀 What You’ll Learn in This Guide"):
        st.markdown("""
        - How to write better prompts
        - How temperature affects creativity
        - How to spot and avoid hallucinations
        - How to save on API costs
        - How to use LLMs ethically

        Use the **menu on the left** to explore each topic.
        """)

elif selected == "Prompt Engineering":
    st.header("🧠 Prompt Like a Pro")
    sub = st.selectbox("Choose a sub-topic:", ["All", "What is a Prompt?", "Best Practices", "Try It Yourself"])

    if sub == "All" or sub == "What is a Prompt?":
        with custom_expander("🔍 What is a Prompt?"):
            st.markdown("A **prompt** is the text you give to an AI model to guide its response. The clearer your prompt, the better the output.")

    if sub == "All" or sub == "Best Practices":
        with custom_expander("🛠️ Best Practices"):
            st.markdown("""
            - Be **specific**: "Write a 2-sentence product description for a pet food startup."
            - Set a **role**: "You are a copywriter for eco-brands..."
            - Define the **output format**: "Return as bullet points."
            """)

    if sub == "All" or sub == "Try It Yourself":
        with custom_expander("✍️ Try it Yourself"):
            user_prompt = st.text_area("Enter a prompt you'd use for your business:", "Write a catchy product description for a new app that tracks sleep patterns.")
            if user_prompt:
                st.markdown(f"_Example result (simulated):_\n\n> \"{user_prompt.replace('Write a', 'Introducing our new tool that helps you')}\"")

elif selected == "Temperature & Sampling":
    st.header("🎛️ Controlling AI Creativity")
    sub = st.selectbox("Choose a sub-topic:", ["All", "What is Temperature?", "Live Example"])

    if sub == "All" or sub == "What is Temperature?":
        with custom_expander("🔥 What is Temperature?"):
            st.markdown("""
            Temperature controls how **random** or **creative** the AI’s response will be:
            - `0.0` = Very precise and repetitive (good for factual answers)
            - `0.7` = Balanced creativity (good for writing copy)
            - `1.0` = Very creative and varied (good for brainstorming)
            """)

    if sub == "All" or sub == "Live Example":
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
    st.markdown("Sometimes, LLMs make up facts or details. This is called a **hallucination**.")

    with custom_expander("🧠 Why It Happens"):
        st.markdown("LLMs predict text based on patterns in data. They do not \"know\" truth — they generate what sounds plausible.")

    with custom_expander("🚫 Example"):
        st.markdown("""
        **Prompt:** "What’s the latest GDPR certification for startups?"

        **LLM Output:** "The 2024 GDPR-AI Gold Standard certification…" ❌ _(this does not exist)_
        """)

    with custom_expander("✅ Best Practices"):
        st.markdown("""
        - Cross-check AI outputs with trusted sources
        - Use LLMs for drafting, not verifying
        - Add human review for published content
        - Avoid using LLMs to generate legal or financial advice
        """)

elif selected == "API Cost Optimization":
    st.header("💸 Saving Money with LLM APIs")
    with custom_expander("📉 Why It Matters"):
        st.markdown("""
        - GPT-4 is powerful but expensive
        - Longer prompts and outputs = more tokens
        - Every API call has a cost
        """)

    with custom_expander("💰 Strategies to Reduce Cost"):
        st.markdown("""
        - Use **GPT-3.5** for non-critical tasks
        - Keep prompts **short and efficient**
        - **Batch** multiple tasks into one call
        - Use **caching** for repeated requests
        """)

    with custom_expander("📊 Cost Example"):
        st.markdown("""
        - 100 calls to GPT-4 at 500 tokens each = ~$3
        - 100 calls to GPT-3.5 = ~$0.20
        """)

elif selected == "Ethics & Bias":
    st.header("⚖️ Responsible AI Use for Startups")
    with custom_expander("⚠️ What’s the Risk?"):
        st.markdown("""
        - LLMs can reflect or amplify **biases** in their training data
        - Outputs can reinforce **stereotypes** or generate **harmful assumptions**
        """)

    with custom_expander("🧪 Example"):
        st.markdown("""
        **Prompt:** "Describe a CEO."

        **Output:** "He is a confident leader..." ❌ _(gender bias)_
        """)

    with custom_expander("🛡 How to Mitigate"):
        st.markdown("""
        - Use **inclusive language** in your prompts
        - **Test outputs** for bias before publishing
        - Document your AI usage policies
        - Understand your **legal obligations** (GDPR, AI Act)
        """)

elif selected == "FAQs":
    st.header("❓ Frequently Asked Questions")
    with custom_expander("What is a language model?"):
        st.write("An LLM is an AI system trained to understand and generate human-like text.")
    with custom_expander("What is a token?"):
        st.write("A token is a chunk of text (word or part-word) used in LLMs. Cost is often based on token count.")
    with custom_expander("Can I trust the output?"):
        st.write("LLMs are not always accurate. Always verify important information.")
    with custom_expander("Is GPT-3.5 enough for my startup?"):
        st.write("Usually yes! It’s cheaper and performs well for most use cases.")

elif selected == "Glossary":
    st.header("📖 Glossary of Common Terms")
    terms = {
        "LLM": "Large Language Model",
        "Token": "Smallest unit of input text processed by an AI model",
        "Prompt": "Instruction or input text given to an AI",
        "Temperature": "Controls randomness in AI output",
        "Hallucination": "AI-generated false or fabricated information",
        "Bias": "Systematic unfairness in output based on training data"
    }
    for term, definition in terms.items():
        st.markdown(f"**{term}** — {definition}")

elif selected == "Interactive Use Cases":
    st.header("🧪 AI Use Case Simulator")
    use_case = st.selectbox("Choose a scenario:", ["Product Description", "Customer Support Reply", "Marketing Email"])

    if use_case == "Product Description":
        product = st.text_input("Describe your product:", "Eco-friendly water bottle with temperature sensor")
        if product:
            st.success(f"Example Output: Meet your new hydration hero – {product}, built to keep you cool and sustainable.")

    elif use_case == "Customer Support Reply":
        issue = st.text_area("Enter the customer issue:", "The app is not tracking my sleep correctly.")
        if issue:
            st.success(f"Example Response: We're sorry to hear that! Our team is looking into this issue: '{issue}'. Please try reinstalling and contact us if it persists.")

    elif use_case == "Marketing Email":
        offer = st.text_input("What's your campaign about?", "10% off all subscriptions this month")
        if offer:
            st.success(f"Example Email: Unlock your {offer}! Our smart tools are now even more affordable. Don't miss out – offer ends soon!")

elif selected == "Download Toolkit":
    st.header("📦 Downloadable Toolkit")
    toolkit = """
    LLM Guide for Startups - Quick Toolkit

    PROMPT ENGINEERING:
    - Be specific
    - Assign a role
    - Ask for a format

    TEMPERATURE:
    - 0.0 = factual, 1.0 = creative

    HALLUCINATIONS:
    - Cross-check outputs
    - Don’t rely for legal/medical info

    COST TIPS:
    - Use GPT-3.5 when possible
    - Keep prompts short
    - Batch and cache

    ETHICS:
    - Use inclusive language
    - Test for bias
    - Know your legal obligations
    """
    st.download_button("📥 Download Toolkit as TXT", data=toolkit, file_name="llm_startup_toolkit.txt")

elif selected == "Feedback":
    st.header("💬 We Value Your Feedback")

    st.markdown("""
    **Thanks for exploring our guide on *Smart Startups, Smarter AI*!**  
    We'd love to know how useful you found it — give us a rating from **1 (Not useful)** to **5 (Extremely useful)**.  
    Your feedback helps us refine and expand this resource for fellow entrepreneurs.  
    """)

    # Input fields
    name = st.text_input("Your name *")
    email = st.text_input("Want a follow-up? Enter your email (optional):")
    rating = st.slider("How helpful was this guide?", 1, 5, 3)
    feedback = st.text_area("Your thoughts (optional)")

    suggestion = st.selectbox(
        "What would you like to see next from us? (optional)",
        [
            "None",
            "LLM APIs for Startups",
            "Cost Optimization",
            "Using LLMs in Customer Support",
            "Startup AI Tools Comparison",
            "No-code LLM Prototyping"
        ]
        index=0
    )

    attachment = st.file_uploader("📎 Attach a file (optional)", type=["png", "jpg", "pdf", "txt", "docx"])

    # Email validation
    def is_valid_email(email_str):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email_str)

    # Form validation
    required_filled = bool(name.strip())
    email_valid = True if not email.strip() else is_valid_email(email.strip())
    form_valid = required_filled and email_valid

    if st.button("Submit Feedback", disabled=not form_valid):
        if not email_valid:
            st.error("Please enter a valid email address.")
        elif not name.strip():
            st.error("Name is required.")
        else:
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
            st.success(f"Thanks {name.strip()} for your feedback! We’ll use your input to improve the experience.")

    # Show feedback if available
    if st.session_state['feedback']:
        if st.checkbox("Show All Feedback"):
            df = pd.DataFrame(st.session_state['feedback'])
            df.columns = [col.capitalize() for col in df.columns]
            st.dataframe(df.style.hide(axis="index"))

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
