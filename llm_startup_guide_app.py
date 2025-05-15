import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import pandas as pd
import re
import os
import requests

# --- App Config ---
st.set_page_config(page_title="LLM Guide for Startups", layout="wide")

# --- Load CSS ---
css_path = "WebAppstyling.css"  # Use enhanced version
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("CSS file not found. Styling will be minimal.")
    
if "read_sections" not in st.session_state:
    st.session_state["read_sections"] = set()
    

# --- File Path for Feedback ---
FEEDBACK_PATH = "feedback.csv"

# --- Load Feedback ---
@st.cache_data(ttl=3600)
def load_feedback(path=FEEDBACK_PATH):
    """Load feedback from CSV if available, else return empty list."""
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            return df.to_dict("records")
        except Exception as e:
            st.error(f"Error loading feedback: {str(e)}")
            return []
    return []

if 'current_page_index' not in st.session_state:
    st.session_state['current_page_index'] = 0  # Used for navigation, optional
    
if st.form_submit_button("expand"):
    st.session_state["expand_button_clicked"] = True
if st.form_submit_button("collapse"):
    st.session_state["collapse_button_clicked"] = True

# --- Utility Functions ---
def expander_section(title):
    key = f"expander_{title}"

    # Set initial state if not already present
    if key not in st.session_state:
        st.session_state[key] = False

    # Respect global toggle once, then reset it
    if st.session_state.get("global_expansion_state") is not None:
        st.session_state[key] = st.session_state["global_expansion_state"]

    return st.expander(title, expanded=st.session_state[key])

def display_expand_collapse_controls(current_page: str):
    visible_on_pages = [
        "Home", "Prompt Engineering", "Temperature & Sampling", "Hallucinations",
        "API Cost Optimization", "Ethics & Bias", "FAQs", "Glossary"
    ]

    if current_page in visible_on_pages:
        st.markdown("""
        <div class='floating-buttons'>
            <form action="" method="post">
                <button name="expand" type="submit">➕ Expand All</button>
                <button name="collapse" type="submit">➖ Collapse All</button>
            </form>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.get("expand_button_clicked"):
            st.session_state["global_expansion_state"] = True
            st.session_state["expand_button_clicked"] = False
            st.rerun()

        if st.session_state.get("collapse_button_clicked"):
            st.session_state["global_expansion_state"] = False
            st.session_state["collapse_button_clicked"] = False
            st.rerun()

def reset_expansion_state():
    if "global_expansion_state" in st.session_state:
        del st.session_state["global_expansion_state"]
        
def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def store_feedback(entry, path=FEEDBACK_PATH):
    """Append new entry to CSV, creating file if it doesn't exist."""
    try:
        new_entry_df = pd.DataFrame([entry])
        if os.path.exists(path):
            existing_df = pd.read_csv(path)
            combined_df = pd.concat([existing_df, new_entry_df], ignore_index=True)
        else:
            combined_df = new_entry_df  # New file
        combined_df.to_csv(path, index=False)
    except Exception as e:
        st.error(f"Error saving feedback: {str(e)}")

# --- Sidebar Navigation ---
page_titles = [
    "Home", "Prompt Engineering", "Temperature & Sampling", "Hallucinations",
    "API Cost Optimization", "Ethics & Bias", "FAQs", "Glossary", "Feedback"
]

with st.sidebar:
    current_page = option_menu(
        menu_title="Sections",
        options=page_titles,
        icons=[
            "house", "pencil", "sliders", "exclamation-circle", "cash-coin", "shield-check",
            "question-circle", "book","envelope"
        ],
        menu_icon="cast"
    )
with st.sidebar:
    st.markdown("### 🔍 Quick ")
    _query = st.text_input(" topics", placeholder="e.g. hallucinations, prompt types")
    
def keyword_matches(query, text):
    return query and query.lower() in text.lower()

all_sections = {
    "Home": list(home_sections.keys()),
    "Prompt Engineering": [
        "What is Prompt and Prompt Engineering?",
        "Types of Prompts",
        "Vague vs. Clear Prompt Examples",
        "Prompt Engineering Best Practices",
        "Common Pitfalls to Avoid",
        "Prompt Engineering vs Prompt Tuning",
        "Prompt Engineering Use Cases for Startups",
        "Learn More: Prompt Engineering Resources",
        "Test Your Knowledge"
    ],
    "Temperature & Sampling": [
        "What is Temperature in Language Models?",
        "What Is Sampling in LLMs?",
        "Adjust the Temperature and See the Difference",
        "Match Temperature to a Task",
        "Temperature Summary Table",
        "Common Misconceptions",
        "Final Takeaway: Use Temperature & Sampling Like Controls"
    ],
    "Hallucinations": [
        "What Are Hallucinations?",
        "Example: Product Fact Gone Wrong",
        "Why Do LLMs Hallucinate?",
        "How to Minimize Hallucinations",
        "Quick Check: Can You Spot the Hallucination?"
    ]
}

if _query:
    st.markdown("### 🔎  Results")
    matches_found = False
    for page, titles in all_sections.items():
        for title in titles:
            if keyword_matches(_query, title):
                matches_found = True
                st.markdown(f"- 🔗 **{title}** (_in {page}_)")

    if not matches_found:
        st.info("No matches found. Try another keyword.")
# --- Home Page ---
if current_page == "Home":
    st.markdown("<h1 style='text-align:center;'>Smart Startups. Smart AI.</h1>", unsafe_allow_html=True)
    display_expand_collapse_controls(current_page)

    # --- Right-side Sub-topic Selector ---
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        st.markdown("### Explore Key Sections")
    with col_right:
        home_subtopic = st.selectbox(
            "Sub-topic",
            [
                "All",
                "Introduction to Large Language Models",
                "How Language Models Work",
                "Why LLMs Matter for Startups",
                "Best Practices & Ethics",
                "Who Should Use This Guide",
                "Let's Get Started!",
            ]
        )
        
    home_sections = {
    "Introduction to Large Language Models": (
        "Large Language Models (LLMs) are smart computer programs that can read, understand, and write text like a human. "
        "They are trained by reading huge amounts of information from books, websites, and articles. "
        "This helps them learn how people use language, so they can help in many useful ways:\n\n"
        "- Answer questions and explain things clearly\n"
        "- Write emails, blog posts, or summaries\n"
        "- Assist with code generation and debugging\n"
        "- Translate between different languages\n"
        "- Support tasks in education, business, and creative work\n\n"
        "**In Simple Terms:**\n"
        "- LLMs power chatbots like ChatGPT, Claude, and Google Gemini.\n"
        "- They’re trained on billions of words from the internet.\n"
        "- Widely used in customer service, education, content creation, and tools."
    ),

    "How Language Models Work": (
        "LLMs are trained using large amounts of text to learn patterns in language. "
        "They don’t understand meaning like humans do — instead, they predict the most likely next word or phrase based on what you type.\n\n"
        "**How LLMs generate text:**\n"
        "- You provide a prompt or question.\n"
        "- The model predicts the next word, again and again, to form a full response.\n"
        "- It uses probabilities learned during training to decide what comes next.\n\n"
        "**What's a token?**\n"
        "- A token is a small piece of text — like a word or part of a word.\n"
        "- For example, “Startup” might become “Start” and “up.”\n"
        "- Most AI tools charge based on the number of tokens processed.\n\n"
        "**Key takeaway:**\n"
        "- LLMs aren’t  engines — they don’t know facts.\n"
        "- They generate likely-sounding responses. Always verify important info!"
    ),

    "Why LLMs Matter for Startups": (
        "Startups often need to move fast with limited resources. LLMs help teams work more efficiently, build smarter tools, and scale faster without needing big teams.\n\n"
        "- Automate customer support and answer FAQs\n"
        "- Write product descriptions, blog posts, and marketing emails\n"
        "- Build chatbots and interactive assistants quickly\n"
        "- Speed up MVP development with code generation and idea testing\n"
        "- Save time on repetitive tasks and re"
    ),

    "Best Practices & Ethics": (
        "Using LLMs wisely ensures safe, fair, and productive outcomes. Here are some key best practices to follow:\n\n"
        "- Write clear, specific prompts for better results\n"
        "- Learn how model temperature affects creativity and accuracy\n"
        "- Don’t rely on AI for factual truth — always double-check\n"
        "- Monitor and manage API usage to control costs\n"
        "- Be aware of potential bias, fairness issues, and ethical concerns"
    ),

    "Who Should Use This Guide": (
        "This guide is built for anyone curious about applying LLMs in a startup or business setting — no technical background required.\n\n"
        "- Startup founders exploring how AI can boost their business\n"
        "- Product managers and developers building AI features\n"
        "- Marketing and content teams looking to scale output\n"
        "- Investors or advisors evaluating AI strategies\n"
        "- Curious learners who want to understand AI in practical terms"
    ),

    "Let's Get Started!": (
        "Use the left menu to explore helpful topics, real use cases, and interactive tools. "
        "You’ll find step-by-step guidance to help you start using AI effectively — whether for writing, coding, customer support, or product development.\n\n"
        "- Browse each section to learn more\n"
        "- Try interactive examples and tools\n"
        "- Get inspired by practical applications for startups\n"
        "- Start small and scale smart with LLMs"
    )
    }
    # --- Render Sections Based on Selection ---
    for title, content in home_sections.items():
        if home_subtopic == "All" or home_subtopic == title:
            with expander_section(title):
                st.markdown(content)

                # --- Enhanced features only for LLM Fundamentals ---
                if title == "How Language Models Work":
                    # Infographic
                    st.image("how_llms_generate_text.png", caption="How LLMs Generate Text", width=400)

                    # Prompt vs Output Example
                    st.markdown("#### Prompt vs. Output Example")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.code("Prompt:\n\"Describe our budgeting app in one sentence.\"", language="text")
                    with col2:
                        st.success("SmartBudget helps freelancers take control of their finances with simple tracking and goal setting.")

                    # Quiz
                    st.markdown("#### Quiz: How Well Do You Understand LLMs?")
                    q1 = st.radio("True or False: LLMs  the internet to answer questions.",
                                  ["-- Select --", "True", "False"], key="llm_q1")
                    if q1 == "False":
                        st.success("Correct! LLMs generate responses from prior training, not live web access.")
                    elif q1 == "True":
                        st.error("Not quite. LLMs don’t use the internet — they generate likely next words.")

                    # Can vs. Can’t Table
                    st.markdown("#### What LLMs Can & Can’t Do")
                    st.markdown("""
                    | Can Do                              | Cannot Do                         |
                    |-------------------------------------|------------------------------------|
                    | Generate text (e.g. emails, posts)  | Access real-time internet          |
                    | Summarize and rephrase content      | Guarantee factual accuracy         |
                    | Simulate tone or role (e.g. CEO)    | Understand human intent            |
                    | Translate languages                 | Know current events                |
                    """)

        with expander_section(title):
        st.markdown(content)
        st.session_state["read_sections"].add(title)
    
    total_sections = sum(len(s) for s in all_sections.values())
    read_sections = len(st.session_state["read_sections"])
    progress = int((read_sections / total_sections) * 100)

    st.markdown("### Your Reading Progress")
    st.progress(progress)
    st.caption(f"You’ve completed **{read_sections} of {total_sections}** sections ({progress}%)")
    
    reset_expansion_state()

# --- Prompt Engineering Page ---
elif current_page == "Prompt Engineering":
    st.title("Prompt Like a Pro")
    display_expand_collapse_controls(current_page)

    col_left, col_right = st.columns([3, 1])

    with col_left:
        st.markdown("### Prompt Engineering Insights")
    with col_right:  
        subtopic = st.selectbox(
            "Sub-topic",
            [
                "All",
                "Introduction to Prompt Engineering",
                "Types of Prompts",
                "Vague vs. Clear Examples",
                "Prompt Best Practices",
                "Common Pitfalls",
                "Prompt Engineering vs Prompt Tuning",
                "Startup Use Cases",
                "Prompt Learning Resources"
                "Quiz",
            ]
        )

    if subtopic in ("All", "Introduction to Prompt Engineering"):
        with expander_section("What is Prompt and Prompt Engineering?"):
            st.markdown("""
            A **prompt** is the instruction you give to an AI model. Think of it like a creative brief — 
            the clearer you are, the better the output.
            
            **Prompt Engineering** is the practice of crafting clear and effective inputs (prompts) to guide large language models (LLMs) like GPT-4.  
            Think of it like writing instructions to a very smart assistant — the better your instructions, the better the output.

            #### Why It Matters for Startups
            -  Speeds up content generation and prototyping
            -  Powers customer support chatbots and assistants
            -  Helps in idea generation, naming, and brainstorming
            -  Reduces reliance on manual copywriting, support, or even coding
            """)
            
    if subtopic in ("All", "Types of Prompts"):
        with expander_section("Types of Prompts"):
            st.markdown("""
            Different types of prompts serve different needs. Here are the most common:

            ####  Zero-shot Prompting
            No examples are provided. The model relies entirely on the instruction.
            - *Example:* "Write a one-line product description for a fitness tracker."

            ####  One-shot Prompting
            A single example is included.
            - *Example:*  
              Q: What’s 2 + 2? A: 4  
              Q: What’s 7 + 5?

            ####  Few-shot Prompting
            Multiple examples help guide the model.
            - *Example:*  
              "Translate: EN: Hello → ES: Hola. EN: Thank you → ES: Gracias."

            #### Instructional vs Conversational
            - **Instructional:** Direct commands like “Summarize this email in 3 lines.”
            - **Conversational:** Framed as a dialogue, e.g., “Hi! Can you help me explain this concept to a 10-year-old?”
            """)
    if subtopic in ("All", "Vague vs. Clear Examples"):
        with expander_section("Vague vs. Clear Prompt Examples"):
            col1, col2 = st.columns(2)
            with col1:
                st.error("Vague Prompt")
                st.markdown("- Describe our app\n- Write something about our new feature")
            with col2:
                st.success(" Clear Prompt")
                st.markdown("- Write a 3-sentence product description...\n- Write a 2-sentence announcement...")

            
    if subtopic in ("All", "Prompt Best Practices"):
        with expander_section("Prompt Engineering Best Practices"):
            st.markdown('''
                Great prompts are clear, structured, and targeted.
                
                ####  Key Techniques
                - **Be Clear & Specific:** Avoid vague instructions.
                - **Use Delimiters:** Separate instructions from content with `"""` or `---`.
                - **Step-by-Step Instructions:** Ask the model to "explain step-by-step" when needed.
                - **Set a Role:** E.g., "You are a technical recruiter."
                - **Define Output Format:** Specify number of bullets, length, tone, etc.
                - **Iterate:** Rerun and refine based on what works.
                
                _Example Prompt:_  
                > "You are a SaaS marketer. Write a 2-sentence announcement for our AI onboarding tool, in a friendly tone."
                ''')
                      
    if subtopic in ("All", "Common Pitfalls"):
        with expander_section("Common Pitfalls to Avoid"):
            st.markdown("""
            Even simple prompts can fail if they're poorly structured. Here are key mistakes to avoid:

            -  **Ambiguity:** “Tell me about our product” — too vague.
            -  **Overloading Instructions:** Don't cram 5 tasks into 1 prompt.
            -  **Missing Context:** Always provide enough background for the model to understand the task.
            """)

    if subtopic in ("All", "Prompt Engineering vs Prompt Tuning"):
        with expander_section("Prompt Engineering vs Prompt Tuning"):
            st.markdown("""
            While both involve improving how AI generates output, they differ significantly:

            - **Prompt Engineering**  
              Uses well-crafted text prompts to control output. No training required. Fast and flexible.

            - **Prompt Tuning (Advanced)**  
              Involves fine-tuning the model on a custom dataset. Requires ML knowledge, compute resources, and time.

            _ Prompt Engineering is ideal for startups needing quick results without deep ML expertise._
            """)
            
    if subtopic in ("All", "Startup Use Cases"):
        with expander_section("Prompt Engineering Use Cases for Startups"):
            st.markdown("""
            Prompt engineering can unlock huge value across startup functions:

            -  **Marketing:** Social media posts, taglines, blog intros
            -  **Customer Support:** Smart autoresponders, refund replies
            -  **Product & Dev:** Auto-generate feature descriptions, bug summaries
            -  **Branding:** Name generation, slogan ideas, elevator pitches
            """)
  

    if subtopic in ("All", "Prompt Learning Resources"):
        with expander_section("Learn More: Prompt Engineering Resources"):
            st.markdown("""
            Dive deeper into the art and science of prompting with these free resources:

            -  [OpenAI Cookbook – Prompting Guide](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb)
            -  [PromptHero (Community Examples)](https://prompthero.com/)
            -  [FlowGPT – Community Prompt Library](https://flowgpt.com/)
            -  [Full Guide to Prompt Engineering](https://www.promptingguide.ai/)
            """)

    if subtopic in ("All", "Quiz"):
        with expander_section("Test Your Knowledge"):
            q1 = st.radio("1. What makes a good prompt?", [
                "-- Select an answer --",
                "Something short like 'Write something'",
                "Clear instructions with role, format, and topic",
                "Anything, the AI will figure it out"
            ])
            if q1 != "-- Select an answer --":
                if q1 == "Clear instructions with role, format, and topic":
                    st.success("Correct!")
                else:
                    st.error("Try again.")

            q2 = st.radio("2. Which is a strong ad prompt?", [
                "-- Select an answer --",
                "Write an ad",
                "Write a 2-line ad copy for a wearable fitness tracker targeting new moms in a friendly tone",
                "Make something catchy"
            ])
            if q2 != "-- Select an answer --":
                if "fitness tracker" in q2:
                    st.success("Spot on!")
                else:
                    st.error("Try again.")

            q3 = st.radio("3. True or False: AI always knows your intent.", [
                "-- Select an answer --",
                "True",
                "False"
            ])
            if q3 != "-- Select an answer --":
                if q3 == "False":
                    st.success("Correct!")
                else:
                    st.error("Incorrect.")
    
    reset_expansion_state()

elif current_page == "Temperature & Sampling":
    st.title("Temperature & Sampling")
    display_expand_collapse_controls(current_page)

    # --- Right-side Subtopic Selector ---
    col_left, col_right = st.columns([3, 1])

    with col_left:
        st.markdown("### Explore Temperature & Sampling Concepts")
    with col_right:
        subtopic = st.selectbox(
            "Sub-topic",
            [
                "All", "What is Temperature?","What is Sampling?", "Adjust the Temperature",
                 "Match Temp to Task", "Summary Table", "Common Misconceptions", "Final Takeaway"
            ]
        )
    if subtopic in ("All", "What is Temperature?"):
        with expander_section("What is Temperature in Language Models?"):
            st.markdown("""
            **Temperature** controls how creative or consistent a language model’s responses are.  
            It ranges from **0.0 (very safe)** to **1.0 (very random)**.

            - **Low (0.1–0.3)** → Factual, predictable, robotic  
            - **Medium (0.4–0.6)** → Natural balance  
            - **High (0.7–1.0)** → Creative, surprising

             Think of temperature as the AI’s **risk-taking slider**.
            """)
            st.info("Tip: For investor summaries or product specs → use low temp. For brainstorming ideas or marketing slogans → use high temp.")
    
    if subtopic in ("All", "What is Sampling?"):
        with expander_section("What Is Sampling in LLMs?"):
            st.write("""
            **Sampling** is how the model decides **which word to say next**. It picks from a range of likely options, not just the top one.

            Two techniques:
            - **Top-k sampling**: From top k most likely next words
            - **Top-p sampling (nucleus sampling)**: From smallest group of words with probability above p

            This helps avoid repetition and create variation — useful for startups generating product copy, blog posts, or email variations.
            """)
    if subtopic in ("All", "Adjust the Temperature"):
        with expander_section("Adjust the Temperature and See the Difference"):
            temp = st.slider("Choose a temperature value", 0.1, 1.0, step=0.1, value=0.7)
            if temp < 0.3:
                st.success("Low Temperature (Factual & Consistent)")
                st.markdown("> Our app helps freelancers manage budgets. It's secure and simple.")
            elif temp < 0.7:
                st.info("Medium Temperature (Balanced & Natural)")
                st.markdown("> Meet your financial sidekick — smart, helpful, and always on call.")
            else:
                st.warning("High Temperature (Creative & Risky)")
                st.markdown("> Money? Managed. Chaos? Cancelled. Our app is your freedom button.")
    
    if subtopic in ("All", "Match Temp to Task"):
            with expander_section("Match Temperature to a Task"):
                st.markdown("""
                | Task                             | Best Temperature | Why                              |
                |----------------------------------|------------------|----------------------------------|
                | Legal docs or product specs      | 0.1 – 0.2        | Needs precision and consistency  |
                | Customer service replies         | 0.3 – 0.5        | Polite, friendly, on-brand       |
                | Blog intros or product stories   | 0.5 – 0.7        | Natural, slightly creative       |
                | Instagram ad or slogan ideas     | 0.8 – 1.0        | Bold, punchy, unexpected         |
                """)

    if subtopic in ("All", "Summary Table"):
        with expander_section("Temperature Summary Table"):
            st.markdown("""
            | Temperature | Output Style       | Best For                            |
            |-------------|--------------------|-------------------------------------|
            | 0.1 – 0.3   | Safe, focused       | Legal disclaimers, investor reports |
            | 0.4 – 0.7   | Balanced, natural   | Product copy, customer FAQs         |
            | 0.8 – 1.0   | Creative, surprising| Marketing, brainstorming, social    |
            """)

    if subtopic in ("All", "Common Misconceptions"):
        with expander_section("Common Misconceptions"):
            st.markdown("""
            |  Myth                                  |  Truth                                               |
            |----------------------------------------|------------------------------------------------------|
            | High temperature = more accurate       | No — it means more *variety*, not accuracy.          |
            | Low temperature is always best         | It’s best only when you want very safe output.       |
            | Sampling doesn’t matter                | It’s crucial for avoiding repetition.                |
            """)

    if subtopic in ("All", "Final Takeaway"):
        with expander_section("Final Takeaway: Use Temperature & Sampling Like Controls"):
            st.markdown("""
             **Quick Guide:**
            - Use **low temperature** for consistent, formal content.
            - Use **high temperature** to ideate, entertain, and experiment.
            - Use **sampling** to keep outputs fresh and natural.

             Your AI is like a co-creator. Adjust temperature and sampling to guide tone and creativity.
            """)

    st.markdown("Adjusting temperature = fine-tuning your **startup's voice**: From steady and formal to bold and creative.")
    if "global_expansion_state" in st.session_state:
        del st.session_state["global_expansion_state"]
    
elif current_page == "Hallucinations":
    st.title("Hallucinations in Language Models")
    display_expand_collapse_controls(current_page)

    # --- Right-side Sub-topic Selector ---
    col_left, col_right = st.columns([3, 1])

    with col_left:
        st.markdown("### Understand and Detect AI Hallucinations")
    with col_right:
        halluc_subtopic = st.selectbox(
            "Sub-topic",
            [
                "All",
                "What Are Hallucinations?",
                "Startup Example",
                "Why It Happens",
                "How to Minimize",
                "Spot the Hallucination (Quiz)"
            ]
        )

    # --- Section Display Logic ---
    if halluc_subtopic in ("All", "What Are Hallucinations?"):
        with expander_section("What Are Hallucinations?"):
            st.write("""
            Hallucinations are **confident but incorrect responses** generated by a language model.

            Even though the response may sound fluent and factual, the model may be **making things up** — especially when it lacks context or isn’t grounded in verified data.
            """)
            st.markdown("""
            A deeper look at hallucinations reveals several types:

            - **Factual Hallucinations**  
              The model provides incorrect facts (e.g., wrong dates, names, or events).  
              _Example: “Stripe was founded in 2015.”_

            - **Citation Hallucinations**  
              The model invents fake sources, URLs, or references.  
              _Example: Linking to a nonexistent re paper._

            - **Logical Hallucinations**  
              The output contains contradictions or flawed reasoning.  
              _Example: “All startups fail, which is why every founder becomes successful.”_
            """)

    if halluc_subtopic in ("All", "Startup Example"):
        with expander_section("Example: Product Fact Gone Wrong"):
            st.write("**Prompt:** “When was Stripe founded?”")
            st.error("**LLM Output:** “Stripe was founded in 2015 in Toronto.” (Incorrect)")
            st.success("**Correct Answer:** Stripe was founded in 2010 in San Francisco.")
            st.warning("For startups, hallucinations can lead to misinforming users, misrepresenting data in pitch decks, or publishing inaccurate content.")

    if halluc_subtopic in ("All", "Why It Happens"):
        with expander_section("Why Do LLMs Hallucinate?"):
            st.write("Language models sometimes produce information that sounds correct but isn't. Here's why:")
            st.markdown("""
            ### Reasons Behind Hallucinations

            - **LLMs generate language based on patterns in training data, not real-time internet access.**  
              They are trained on massive datasets (books, articles, web content), but they can’t browse the internet or fetch live data. They rely solely on what they’ve seen before.

            - **They don’t “know” facts — they predict the next likely word.**  
              These models are not fact-checkers. They generate plausible-sounding sequences of words based on statistical patterns in their training data.

            - **When uncertain, they may fabricate names, dates, citations, or product details.**  
              If a prompt asks for something obscure or ambiguous, the model may guess — producing **fictional yet confident-sounding answers**.
            """)

    if halluc_subtopic in ("All", "How to Minimize"):
        with expander_section("How to Minimize Hallucinations"):
            st.markdown("""
            LLMs are powerful tools, but they can generate **confident-sounding yet incorrect information**. Here’s how to reduce the risk of hallucinations, especially in high-stakes contexts like startup communications, investor decks, or product content.

            ### Recommended Practices

            - **Be specific with prompts:**  
              Avoid vague instructions. Instead, give clear, detailed prompts that provide enough context to steer the model's response.

            - **Use retrieval-based methods (like RAG):**  
              Retrieval-Augmented Generation combines LLMs with live or static knowledge sources (e.g., documents, databases). This grounds outputs in verified facts.

            - **Manually review before publishing externally:**  
              Always treat LLM responses as **first drafts**. For public-facing or critical content, conduct a human review step.

            - **Encourage uncertainty when appropriate:**  
              Ask the model to **cite sources** or include phrases like *“I’m not sure”* when unsure.  
              _Example prompt: “If unsure, say ‘I’m not sure’ rather than guessing.”_
            """)

    if halluc_subtopic in ("All", "Spot the Hallucination (Quiz)"):
        with expander_section("Quick Check: Can You Spot the Hallucination?"):
            q1 = st.radio("Which of the following is most likely a hallucination?",
                        ["-- Select an answer --", "Google was founded in 1998.",
                         "Python was invented by Guido van Rossum.",
                         "OpenAI was acquired by Netflix in 2021."],
                        key="hallucination_q1")
            if q1 != "-- Select an answer --":
                if q1 == "OpenAI was acquired by Netflix in 2021.":
                    st.success("Correct! That never happened — it’s a confident hallucination.")
                else:
                    st.error("Not quite — both other statements are factual.")

    st.markdown("Always treat LLM outputs as **first drafts**, not final answers — especially for investor communications, PR, or technical content.")
    reset_expansion_state()

elif current_page == "API Cost Optimization":
    st.title("API Cost Optimization")
    display_expand_collapse_controls(current_page)

    # --- Right-side Sub-topic Selector ---
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        st.markdown("### Build Smart, Spend Smarter")
    with col_right:
        cost_subtopic = st.selectbox(
            "Sub-topic",
            [
                "All",
                "What Is API Cost?",
                "Why API Costs Matter",
                "What Drives Cost",
                "Optimization Strategies",
                "Estimate Token Cost",
                "Final Note"
            ]
        )

    # --- Conditional Rendering of Sections ---
    if cost_subtopic in ("All", "What Is API Cost?"):
        with expander_section("What Is API Cost?"):
            st.write("""
            When you use a language model like GPT-3.5 or GPT-4 through an API, you’re charged based on how many tokens you send and receive.

            A **token** is typically 3–4 characters or about 1 word. You are billed for both the prompt you send and the response the model generates.

            Different models have different pricing structures:

            - **GPT-3.5**: around $0.002 per 1,000 tokens
            - **GPT-4**: around $0.06–$0.12 per 1,000 tokens (input and output priced separately)

            ### Example Calculation

            If you send 500 tokens and get back 500 tokens using GPT-4:

            - Total = 1,000 tokens
            - At $0.06 per 1,000 tokens → $0.06 per interaction

            If you make 1,000 such API calls in a day:

            - 1,000 × $0.06 = **$60/day**
            - Monthly = **$1,800/month**

            ### Why It Matters

            For startups running customer chatbots, automating content, or summarizing emails — this cost can add up fast. Understanding how tokens work helps you plan your usage more strategically.
            """)
    if cost_subtopic in ("All", "Why API Costs Matter"):
        with expander_section("Why API Costs Matter for Startups"):
            st.write("""
            Using language models like GPT-4 can get expensive — especially when handling lots of requests, long prompts, or frequent usage.

            Startups must be **smart and efficient** when building with LLMs, balancing quality with cost.
            """)

    if cost_subtopic in ("All", "What Drives Cost"):
        with expander_section("What Drives API Cost?"):
            st.markdown("""
            - **Token usage** – You pay per word (input + output tokens).  
            - **Model selection** – GPT-4 is powerful but much costlier than GPT-3.5.  
            - **Request frequency** – More requests = more expense.  
            - **Advanced features** – Streaming, tool use, and chaining can add overhead.  
            """)

    if cost_subtopic in ("All", "Optimization Strategies"):
        with expander_section("Optimization Strategies for Founders"):
            st.markdown("""
            1. **Shorten prompts**: Remove unnecessary words and boilerplate.  
            2. **Cache outputs**: Reuse responses for repeated or similar queries.  
            3. **Use cheaper models for simpler tasks**:  
                - GPT-3.5 for summarization, formatting, and basic Q&A.  
                - GPT-4 for critical reasoning and edge-case handling.  
            4. **Batch your inputs**: Send multiple queries in a single call when possible.  
            5. **Think like a product manager**:  
                - Only use AI where it **adds value**.  
                - Avoid using LLMs as your database or source of truth.  
            """)

    if cost_subtopic in ("All", "Estimate Token Cost"):
        with expander_section("Estimate Token Cost"):
            tokens = st.slider("How many tokens per request?", min_value=100, max_value=2000, step=100, value=500)
            requests = st.slider("How many requests per day?", min_value=1, max_value=5000, step=50, value=1000)
            model = st.radio("Select model:", ["GPT-3.5 ($0.002 / 1K tokens)", "GPT-4 ($0.06 / 1K tokens)"])

            cost_per_1k = 0.002 if "3.5" in model else 0.06
            daily_cost = (tokens * requests / 1000) * cost_per_1k
            monthly_cost = daily_cost * 30

            st.success(f"Estimated Monthly Cost: **${monthly_cost:,.2f}**")

    st.markdown("Use logs and dashboards to track usage and refine prompts. Optimizing your AI usage = extending your runway.")
    reset_expansion_state()
    
elif current_page == "Ethics & Bias":
    st.title("Ethics and Bias in Language Models")
    display_expand_collapse_controls(current_page)

    # --- Right-side Sub-topic Selector ---
    col_left, col_right = st.columns([3, 1])

    with col_left:
        st.markdown("### Building Responsible AI for Startups")
    with col_right:
        ethics_subtopic = st.selectbox(
            "Sub-topic",
            [
            "All",
            "Why Ethics and Fairness Matter",
            "Types of Bias",
            "Examples of Bias",
            "Why Bias Happens",
            "What Founders Can Do",
            "Bias Detection Example",
            "Bias Reflection Quiz",
            "Ethical Review Template"
            ]
        )

    # --- Conditional Sections ---
    if ethics_subtopic in ("All", "Why Ethics and Fairness Matter"):
        with expander_section("Why Ethics and Fairness Matter"):
            st.write("""
            Language models are incredibly powerful — but they’re not perfect.

            Since they are trained on vast amounts of internet data, they can reflect social and cultural biases. These biases can unintentionally affect your startup's messaging, hiring tools, or customer communication systems.

            As a founder, you’re responsible for building inclusive and trustworthy experiences.
            """)
            
    if ethics_subtopic in ("All", "Types of Bias"):
        with expander_section("Types of Bias in AI"):
            st.markdown("AI systems can unintentionally reflect and reinforce societal biases present in the data they are trained on. Below are key types of bias that LLMs may exhibit:")

            st.markdown("#### Gender Bias")
            st.write("""
            Assigning roles or characteristics based on traditional gender stereotypes.  
            _Example: Associating “nurse” predominantly with women and “engineer” with men._
            """)

            st.markdown("#### Racial Bias")
            st.write("""
            Producing different outcomes or assumptions based on race.  
            _Example: Facial recognition systems misidentifying individuals from certain racial backgrounds more frequently._
            """)

            st.markdown("#### Cultural Bias")
            st.write("""
            Favoring dominant cultural norms, values, or perspectives, which can marginalize others.  
            _Example: AI-generated advice assuming Western holidays or customs by default._
            """)

            st.markdown("#### Age Bias")
            st.write("""
            Making assumptions about a person’s capabilities or interests based on age.  
            _Example: Assuming older adults are unfamiliar with technology or younger users lack business acumen._
            """)

            st.markdown("#### Language Bias")
            st.write("""
            Preferring specific dialects, grammar, or phrasing — often standard or formal English — while devaluing regional accents, slang, or non-native usage.  
            _Example: Penalizing informal tone or regional expressions in AI content moderation._
            """)

            st.markdown("---")
            st.info("Bias can be subtle or overt. Always test AI outputs across different user personas to catch unintended bias.")

    if ethics_subtopic in ("All", "Examples of Bias"):
        with expander_section("Examples of Bias in AI"):
            st.markdown("""
            - A resume-screening assistant that favors male candidates based on historical hiring data.  
            - A chatbot that assumes all engineers are men.  
            - A product description generator that omits diverse customer personas.  
            """)

    if ethics_subtopic in ("All", "Why Bias Happens"):
        with expander_section("Why Bias Happens in Language Models"):
            st.write("""
            Language models learn from patterns in public text data — books, websites, social media, forums. This means:
            - They may repeat harmful stereotypes.  
            - They often reflect dominant voices more than marginalized ones.  
            - They don't understand fairness — they reproduce frequency patterns in data.  
            """)

    if ethics_subtopic in ("All", "What Founders Can Do"):
        with expander_section("What Startup Founders Can Do"):
            st.markdown("""
            - Test outputs for different demographic or geographic user profiles.  
            - Avoid using AI tools blindly in hiring, lending, or content moderation.  
            - Review all AI-generated content before using it externally.  
            - Add a disclaimer or human review step for sensitive outputs.  
            - Be transparent with users when AI is involved in decisions.  
            """)
            st.markdown("** Downloadable Bias Prevention Checklist:**")
            checklist_content = (
                "Bias Prevention Checklist:\n"
                "- Test outputs for multiple user profiles\n"
                "- Flag outputs with harmful stereotypes\n"
                "- Apply manual review to sensitive use cases\n"
                "- Maintain transparency in AI decision-making\n"
                "- Regularly update prompts or models for fairness\n"
            )
            st.text(checklist_content)
            st.download_button("📥 Download Checklist (TXT)", checklist_content, file_name="bias_checklist.txt")
            
    if ethics_subtopic in ("All", "Bias Detection Example"):
        with expander_section("Live Example: Can You Detect the Bias?"):
            example_prompt = st.selectbox("Choose a prompt", [
                "Write a job ad for a software engineer",
                "Describe a CEO of a tech startup",
                "Introduce a nurse character in a story"
            ])

            biased_outputs = {
                "Write a job ad for a software engineer": "We're looking for a strong, young male developer to join our elite dev team.",
                "Describe a CEO of a tech startup": "He is a brilliant visionary leading a disruptive fintech company.",
                "Introduce a nurse character in a story": "She is a caring young woman who loves to help others."
            }

            st.warning(f"Model Output: “{biased_outputs[example_prompt]}”")
            st.markdown("**Reflection:** Are assumptions being made? Who is being stereotyped or excluded?")

    if ethics_subtopic in ("All", "Bias Reflection Quiz"):
        with expander_section("Try This"):
            bias_prompt = st.radio("Which of these might reflect bias?", [
                "-- Select an answer --",
                "Write a bio for a doctor: 'Dr. Smith is a brilliant young man...'", 
                "Summarize a product spec for a software tool", 
                "Generate a welcome message for a task management app"
            ])
            if bias_prompt == "Write a bio for a doctor: 'Dr. Smith is a brilliant young man...'":
                st.success(" Correct. This assumes the doctor's gender, which may reflect bias.")
            else:
                st.info("This seems neutral, but it's still good practice to evaluate outputs for hidden bias.")

    if ethics_subtopic in ("All", "Ethical Review Template"):
        with expander_section(" Ethical Review Template (For Startups)"):
            st.markdown("### What Is This Template?")
            st.write("""
            This is a structured form to help startup teams evaluate whether an AI-powered feature is being designed and used ethically and responsibly.
            It’s useful for catching potential risks early — like bias, misinformation, or lack of transparency.
            """)
    
            st.markdown("### When Should You Use It?")
            st.markdown("""
            - When building any new feature that involves LLMs or AI-generated content  
            - Before launching customer-facing AI functionality  
            - During internal QA or product review meetings  
            """)
    
            st.markdown("### How to Use It")
            st.write("""
            Complete the form below as a team (product, design, engineering).  
            Save or export the answers as part of your product documentation or AI governance records.
            """)
            
            st.markdown("### Why It’s Useful for Startups")
            st.write("""
                - Helps meet ethical and legal expectations early in your product lifecycle
                - Builds trust with your users and investors
                - Prevents future reputational or legal risk
                - Encourages intentional, responsible design decisions
                """)
    
            with st.form("embedded_ethical_review_form"):
                st.subheader("🔍 Ethical Review Form")
    
                col1, col2 = st.columns(2)
                with col1:
                    feature_name = st.text_input("Feature Name")
                    bias_tested = st.radio("Bias Testing Completed?", ["Yes", "No"])
                    human_review = st.radio("Human Review Process in Place?", ["Yes", "No"])
                with col2:
                    risk_level = st.selectbox("Final Risk Assessment", ["Low", "Medium", "High"])
                    disclosure = st.radio("Disclosure to Users?", ["Yes", "No"])
    
                purpose = st.text_area("Purpose of AI Usage")
                risks = st.text_area("Potential Ethical Risks (e.g., bias, exclusion, hallucination)")
    
                submitted = st.form_submit_button("Submit Review")
    
                if submitted:
                    st.success("Review submitted. Please copy or document your answers for records.")
                    st.markdown("### 📄 Review Summary")
                    st.write(f"**Feature Name:** {feature_name}")
                    st.write(f"**Purpose:** {purpose}")
                    st.write(f"**Potential Risks:** {risks}")
                    st.write(f"**Bias Testing Completed:** {bias_tested}")
                    st.write(f"**Human Review In Place:** {human_review}")
                    st.write(f"**Disclosure to Users:** {disclosure}")
                    st.write(f"**Final Risk Assessment:** {risk_level}")
    
            st.caption("Note: This form is not stored. Copy your review for team documentation or export manually.")
        st.markdown("Fairness in AI isn't just about compliance — it's about creating a startup culture users can trust.")
    reset_expansion_state()
    
elif current_page == "FAQs":
    st.title("Frequently Asked Questions")
    display_expand_collapse_controls(current_page)

    st.header("LLMs for Startup Founders")
    st.markdown("Below are some common questions about using language models like ChatGPT in startup settings:")

    with expander_section("What is a large language model (LLM)?"):
        st.write("A large language model (LLM) is an AI system trained to generate and understand human-like text. It can help you write, summarize, explain, and automate content in your startup workflows.")

    with expander_section("Is ChatGPT the same as a  engine?"):
        st.write("No. ChatGPT doesn’t  the internet live. It generates responses based on patterns learned from training data. It doesn’t verify facts, so double-check anything important.")

    with expander_section("Why does it sometimes say things that are wrong?"):
        st.write("This is called a hallucination. The model doesn’t know what’s true — it just predicts what sounds right. Always review AI-generated content before using it externally.")

    with expander_section("How can I control the tone or creativity of the AI's response?"):
        st.write("Use the temperature setting. Lower values (e.g., 0.2) generate more factual, safe content. Higher values (e.g., 0.8) create more creative or varied outputs.")

    with expander_section("Will using LLMs increase my startup’s costs?"):
        st.write("It can. LLMs charge based on token usage. Use prompt optimization, shorter outputs, model tiering (e.g., GPT-3.5 over GPT-4), and batch processing to control costs.")

    with expander_section("Can I use LLMs for decisions like hiring or pricing?"):
        st.write("Only with caution. LLMs can reflect social bias and make mistakes. Never automate high-stakes decisions without human review.")

    with expander_section("How do I avoid biased or exclusionary outputs?"):
        st.write("Test prompts using diverse scenarios. Be mindful of wording that assumes gender, age, or culture. Use a review process before publishing AI-generated content.")

    st.markdown("Have more questions? Use the **Add a feedback on the site to help us expand this section.")
    reset_expansion_state()

elif current_page == "Glossary":
    st.title("Glossary")
    display_expand_collapse_controls(current_page)

    glossary = {
        "LLM (Large Language Model)": "An AI model trained on vast text datasets to generate and understand human-like language. Examples include GPT-3.5 and GPT-4.",
        "Prompt": "The instruction or input you give to the AI model. Clear, specific prompts produce better results.",
        "Prompt Engineering": "The practice of crafting clear and effective inputs to guide large language models and achieve high-quality outputs.",
        "Zero-shot Prompting": "A prompt format that provides no examples — the model relies solely on the instruction.",
        "Few-shot Prompting": "A prompt that includes multiple examples to guide the model’s responses more effectively.",
        "Instructional Prompt": "A direct command, like 'Summarize this email in three bullet points.'",
        "Conversational Prompt": "A friendly, dialogue-based prompt like 'Hi! Can you help me explain this to a 10-year-old?'",
        "Temperature": "A setting that controls how predictable or creative the model’s output is. Lower = more deterministic, Higher = more diverse.",
        "Token": "A unit of text (like a word or subword). AI models process and charge based on tokens.",
        "Sampling": "A method for selecting which word comes next. Includes top-k and top-p (nucleus) sampling to control randomness.",
        "Top-k Sampling": "The model picks from the top k most likely next tokens.",
        "Top-p Sampling (Nucleus Sampling)": "The model selects from the smallest group of tokens whose cumulative probability is above a threshold p.",
        "Hallucination": "When a language model outputs a confident but incorrect or made-up statement.",
        "Bias": "Unintended favoritism or prejudice in model outputs, usually inherited from biased training data.",
        "Human-in-the-Loop": "A method where humans validate or oversee AI-generated outputs, especially for sensitive tasks.",
        "Model Selection": "Choosing the right AI model based on cost, capability, and complexity — e.g., GPT-4 vs FLAN-T5.",
        "Prompt Tuning": "An advanced technique that fine-tunes prompts using gradient-based optimization and training data.",
        "Use Case": "A real-world application of LLMs to solve a specific startup or business need (e.g., customer support, content generation).",
        "API Token Cost": "The pricing structure based on the number of input and output tokens processed by the model.",
        "Cost Optimization": "Strategies to reduce the cost of using AI APIs, such as shortening prompts and using cheaper models.",
        "Hallucination Risk": "The likelihood of a model generating inaccurate or fabricated content.",
        "Ethical AI": "The practice of using AI responsibly by reducing bias, ensuring fairness, and protecting user trust.",
        "Bias Checklist": "A list of considerations for detecting and minimizing bias in AI outputs or prompts.",
        "Prompt Generator": "A tool that suggests high-quality prompts for specific business or startup needs.",
        "Startup Use Case Matcher": "An interactive tool that recommends LLM use cases based on industry, goal, and team size.",
        "Temperature Control": "The process of tuning the model’s output randomness using the temperature parameter.",
        "Try it Yourself": "An interactive section where users can test prompts and view real-time LLM responses.",
        "Toolkit": "A downloadable collection of templates, guides, and resources for implementing LLMs in startups."
    }

    for term, definition in glossary.items():
        with expander_section(f"**{term}**"):
            st.markdown(f"{definition}")
    reset_expansion_state()
        
elif current_page == "Feedback":
    st.title(" Share Your Experience")
    st.markdown("""
        Your feedback helps us improve the **LLM Guide for Startups**.  
        Let us know what you found useful and what you'd like to see next.
    """)

    st.markdown("### Feedback Form")

    # --- Input Form ---
    with st.form("feedback_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", placeholder="Enter your full name")
        with col2:
            email = st.text_input("Email Address (optional)", placeholder="e.g. alex@startup.ie")

        rating = st.slider(" How helpful was this guide?", 1, 5, 3)
        feedback = st.text_area("Your Comments (optional)", placeholder="What worked well? What could be improved?")
        suggestion = st.selectbox("What topics should we cover next?", 
                                  ["None", "LLM APIs", "Customer Support", "Tool Comparisons", "No-code Prototyping"])
        attachment = st.file_uploader("📎 Optional File Upload", type=["png", "jpg", "pdf", "txt", "docx"])

        required_filled = bool(name.strip())
        email_valid = True if not email.strip() else re.match(r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,}$", email.strip())

        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            if not required_filled:
                st.warning("Please enter your name to submit the form.")
            elif not email_valid:
                st.error("Invalid email format. Please check and try again.")
            else:
                entry = {
                    "Name": name.strip(),
                    "Email": email.strip(),
                    "Rating": rating,
                    "Feedback": feedback.strip(),
                    "Suggested topic": None if suggestion == "None" else suggestion,
                    "Attachment name": attachment.name if attachment else None
                }
                store_feedback(entry)
                st.success(f" Thank you, {name.strip()}! We truly appreciate your insights and will use your feedback to make this guide even better.")
                
                # Refresh entries in session state
                st.session_state['feedback_entries'] = load_feedback()

    # --- Load Feedback into Session If Not Present ---
    if 'feedback_entries' not in st.session_state:
        st.session_state['feedback_entries'] = load_feedback()

    # --- Show Feedback ---
    if st.session_state['feedback_entries']:
        df = pd.DataFrame(st.session_state['feedback_entries'])
    
        # Filter out admin entries and blanks
        df = df[df["Name"].str.strip().str.lower() != "admin"]
        df = df[df["Name"].str.strip() != ""]
    
        df.index += 1
        df.index.name = "No."
        st.markdown("### All Submitted Feedback")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No feedback submitted yet. Be the first to contribute!")

    # --- Admin Controls ---
    with st.expander("Admin Controls: Manage Feedback Records"):
        st.markdown("Export or delete all feedback entries below.")
    
        admin_key_input = st.text_input("Admin Passphrase", type="password", placeholder="Enter passphrase")
        confirm_clear = st.checkbox("I confirm this action is irreversible.")
        ADMIN_PASSPHRASE = st.secrets["ADMIN_PASSPHRASE"]
    
        # Download CSV if entries exist
        if st.session_state.get("feedback_entries"):
            export_df = pd.DataFrame(st.session_state["feedback_entries"])
            csv_data = export_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Feedback CSV", csv_data, file_name="feedback_backup.csv", mime="text/csv")
    
        # Delete all feedback
        if st.button("🗑️ Clear All Feedback"):
            if admin_key_input == ADMIN_PASSPHRASE and confirm_clear:
                try:
                    # Delete the file if it exists
                    if os.path.exists(FEEDBACK_PATH):
                        os.remove(FEEDBACK_PATH)
                        st.success("feedback.csv file deleted from disk.")
                    else:
                        st.info("feedback.csv file not found. Nothing to delete.")
    
                    # Clear session + cached data
                    st.session_state["feedback_entries"] = []
                    st.cache_data.clear()  # Clear any cached CSV load
                    st.success("All feedback entries cleared from memory and cache.")
                    st.rerun()
    
                except Exception as e:
                    st.error(f"Error while deleting feedback: {str(e)}")
            else:
                st.error("Invalid passphrase or confirmation checkbox not selected.")

# --- Compact Unified Footer ---
st.markdown("""---""")

st.markdown("""
<div style='font-size: 16px; line-height: 1.6;'>
    <strong>LLM Guide for Startups</strong> — Practical insights for using language models responsibly and efficiently in startup settings.<br><br>
    Built with by:<br>
    • <strong>Vaishnavi Kandikonda</strong> (24216940) — <a href="mailto:vaishnavi.kandikonda@ucdconnect.com">vaishnavi.kandikonda@ucdconnect.com</a><br>
    • <strong>Shivani Singh</strong> (24234516) — <a href="mailto:shivani.singh@ucdconnect.ie">shivani.singh@ucdconnect.ie</a><br>
    • <strong>Kushal Pratap Singh</strong> (24205476) — <a href="mailto:kushal.singh@ucdconnect.ie">kushal.singh@ucdconnect.ie</a><br>
</div>
""", unsafe_allow_html=True)

st.caption(
    f"© 2025 LLM Startup Guide • Last updated {datetime.now().strftime('%Y-%m-%d')} • Built with Streamlit • Guided by principles of transparency, fairness, and human-centered AI."
)
