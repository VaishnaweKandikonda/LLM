import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import pandas as pd
import re
import os
import random
import requests

# --- App Config ---
st.set_page_config(page_title="LLM Guide for Startups", layout="wide")

# --- Load CSS ---
if os.path.exists("WebAppstyling.css"):
    with open("WebAppstyling.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
# --- Hugging Face API Key ---
HUGGINGFACE_API_KEY = st.secrets["HUGGINGFACE_API_KEY"]

# --- Session State ---
@st.cache_data(ttl=3600)
def load_feedback(path="feedback.csv"):
    return pd.read_csv(path).to_dict("records") if os.path.exists(path) else []

if 'feedback_entries' not in st.session_state:
    st.session_state['feedback_entries'] = load_feedback()

if 'current_page_index' not in st.session_state:
    st.session_state['current_page_index'] = 0

if 'global_expansion_state' not in st.session_state:
    st.session_state['global_expansion_state'] = None

# --- Utility Functions ---
def expander_section(title):
    expanded = st.session_state['global_expansion_state'] if st.session_state['global_expansion_state'] is not None else False
    return st.expander(title, expanded=expanded)

def display_expand_collapse_controls(current_page: str):
    visible_on_pages = [
        "Home", "Prompt Engineering", "Temperature & Sampling", "Hallucinations",
        "API Cost Optimization", "Ethics & Bias"
    ]

    if current_page in visible_on_pages:
        st.markdown("""
            <div class="exp-control-buttons">
                <form action="" method="post">
                    <button name="expand_action" value="expand">➕</button>
                    <button name="expand_action" value="collapse">➖</button>
                </form>
            </div>
        """, unsafe_allow_html=True)

        expand_action = st.query_params.get("expand_action", None)
        if expand_action == "expand":
            st.session_state['global_expansion_state'] = True
        elif expand_action == "collapse":
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
            "https://api-inference.huggingface.co/models/google/flan-t5-small",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            result = response.json()
            # flan-t5 returns a list of dicts with 'generated_text'
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "No output generated."), None
            else:
                return str(result), None
        else:
            return None, f"HF API Error {response.status_code}: {response.text}"

    except Exception as e:
        return None, f"Exception: {str(e)}"

# --- Sidebar Navigation ---
page_titles = [
    "Home", "Prompt Engineering", "Temperature & Sampling", "Hallucinations",
    "API Cost Optimization", "Ethics & Bias", "FAQs", "Glossary",
    "Interactive Use Cases", "Download Toolkit", "Feedback"
]

with st.sidebar:
    current_page = option_menu(
        menu_title="Sections",
        options=page_titles,
        icons=[
            "house", "pencil", "sliders", "exclamation-circle", "cash-coin", "shield-check",
            "question-circle", "book", "tools", "download", "chat-dots","far fa-question-circle"
        ],
        menu_icon="cast"
    )

# --- Home Page ---
if current_page == "Home":
    st.markdown("<h1 style='text-align:center;'>Smart Startups. Smart AI.</h1>", unsafe_allow_html=True)
    display_expand_collapse_controls(current_page)

    home_sections = {
        "Introduction to Large Language Models": (
            "Large Language Models (LLMs) are advanced AI systems trained to understand and generate human-like text. "
            "Popular platforms like ChatGPT, Claude, and Gemini use LLMs to assist users with content generation, problem-solving, and more."
        ),
        "Why LLMs Matter for Startups": (
            "- Automate customer support and FAQs\n"
            "- Generate pitch decks, emails, blogs, and product content\n"
            "- Build intelligent prototypes and chatbots\n"
            "- Accelerate idea validation and MVP development"
        ),
        "Let's Get Started!": (
            "Use the left menu to explore sections packed with insights, use cases, and practical tools to build smarter with AI."
        ),
        "Best Practices & Ethics": (
            "- Learn prompt design for better results\n"
            "- Understand model temperature and creativity\n"
            "- Avoid AI-generated misinformation\n"
            "- Optimize API costs\n"
            "- Navigate bias and fairness responsibly"
        ),
        "Who Should Use This Guide": (
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
    st.title("Prompt Like a Pro")
    display_expand_collapse_controls(current_page)

    st.markdown("### Choose a sub-topic to explore:")
    subtopic = st.selectbox(
        "Select a topic:",
        ["All", "What is a Prompt?", "Best Practices", "Vague vs. Clear Examples",
         "Try it Yourself", "Prompt Use Cases", "Prompt Generator", "Prompt Checklist", "Quiz"]
    )

    if subtopic in ("All", "What is a Prompt?"):
        with expander_section("What is a Prompt?"):
            st.write("""
            A **prompt** is the instruction you give to an AI model. Think of it like a creative brief — 
            the clearer you are, the better the output.
            """)

    if subtopic in ("All", "Best Practices"):
        with expander_section("Best Practices"):
            st.markdown("- Be Specific\n- Set a Role\n- Define Output Format")
            st.success("""
            Example Prompt:\n
            \"Act as a SaaS growth marketer. Write a 2-line social media post in a friendly tone promoting our new AI-based customer onboarding tool.\"
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

    if subtopic in ("All", "Try it Yourself"):
        with expander_section("Try it Yourself"):
            st.markdown("Write a real prompt you'd like to test. We'll generate a response using FLAN-T5.")
            user_prompt = st.text_area("Enter your business prompt:")
            if st.button("Run Prompt") and user_prompt:
                with st.spinner("Generating response..."):
                    response, error = get_llm_response(user_prompt)
            
                if response:
                    st.success(response)
                else:
                    st.error(error)

    if subtopic in ("All", "Prompt Use Cases"):
        with expander_section("What are you using the prompt for?"):
            use_case = st.radio("", ["Marketing", "Customer Support", "Product", "Sales"], horizontal=True)
            suggestions = {
                "Marketing": "Write a tagline for a social media post promoting our product launch.",
                "Customer Support": "Respond to a refund request in a helpful and polite tone.",
                "Product": "Summarize a product spec in under 50 words.",
                "Sales": "Write a follow-up email to a lead who downloaded our whitepaper."
            }
            st.info(f"Try: '{suggestions[use_case]}'")

    if subtopic in ("All", "Prompt Generator"):
        with expander_section("Prompt Generator"):
            samples = [
                "Write a product update email for a budgeting app.",
                "Draft a refund message that is professional.",
                "Create an onboarding message for beta users.",
                "Write an app store description for a sleep tracking app."
            ]
            if st.button("Give me a random prompt"):
                st.write(random.choice(samples))

    if subtopic in ("All", "Prompt Checklist"):
        with expander_section("Prompt Checklist"):
            st.markdown("- Be specific\n- Set a role\n- Define output format")
            
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

elif current_page == "Temperature & Sampling":
    st.title("Temperature & Sampling")
    display_expand_collapse_controls(current_page)

    with expander_section("What is Temperature in Language Models?"):
        st.write("""
        **Temperature** controls how predictable or creative the AI's output is.

        It ranges from **0.0 to 1.0**:
        - A **low temperature** (e.g., 0.1) makes the model **precise, reliable, and factual**.
        - A **high temperature** (e.g., 0.9) makes it **creative, surprising, and more risky**.

        Think of it like this:
        > 0.1 = robotic, safe replies  
        > 0.9 = playful, unexpected ideas
        """)
        st.info("Tip: For investor summaries or product specs → use low temp. For brainstorming ideas or marketing slogans → use high temp.")

    with expander_section("Adjust the Temperature and See the Difference"):
        temperature = st.slider("Select Temperature Level", 0.1, 1.0, 0.7)
        if temperature < 0.3:
            st.success("Low Temperature (Factual & Consistent)")
            st.markdown("Example: “Our app helps freelancers manage budgets. It's secure and simple.”")
        elif temperature < 0.7:
            st.info("Medium Temperature (Balanced)")
            st.markdown("Example: “Meet the financial sidekick for freelancers — smart, helpful, and always on call.”")
        else:
            st.warning("High Temperature (Creative & Risky)")
            st.markdown("Example: “Money? Managed. Chaos? Cancelled. Our app is your financial freedom button.”")

    with expander_section("Temperature Summary Table"):
        st.markdown("""
        | Temperature | Behavior                  | Best For                      |
        |-------------|---------------------------|-------------------------------|
        | 0.1 - 0.3   | Factual, focused, safe    | Reports, investor decks       |
        | 0.4 - 0.7   | Balanced, conversational  | Product copy, onboarding flows|
        | 0.8 - 1.0   | Creative, surprising      | Brainstorms, social content   |
        """)

    with expander_section("What Is Sampling in LLMs?"):
        st.write("""
        **Sampling** is how the model decides **which word to say next**. It picks from a range of likely options, not just the top one.

        Two techniques:
        - **Top-k sampling**: From top k most likely next words
        - **Top-p sampling (nucleus sampling)**: From smallest group of words with probability above p

        This helps avoid repetition and create variation — useful for startups generating product copy, blog posts, or email variations.
        """)

    with expander_section("Match Temperature to a Task"):
        use_case = st.radio("Select your use case:", 
                            ["Summarizing a feature list", "Generating Instagram ad copy", "Writing a refund response email"])
        if use_case == "Summarizing a feature list":
            st.success("Best with: Low Temperature (0.1 - 0.3)")
        elif use_case == "Generating Instagram ad copy":
            st.warning("Best with: High Temperature (0.8 - 1.0)")
        elif use_case == "Writing a refund response email":
            st.info("Best with: Medium Temperature (0.4 - 0.6)")

    st.markdown("Adjusting temperature = fine-tuning your **startup's voice**: From steady and formal to bold and creative.")

elif current_page == "Hallucinations":
    st.title("Hallucinations in Language Models")
    display_expand_collapse_controls(current_page)

    # Intro explanation
    with expander_section("What Are Hallucinations?"):
        st.write("""
        Hallucinations are **confident but incorrect responses** generated by a language model.

        Even though the response may sound fluent and factual, the model may be **making things up** — especially when it lacks context or isn’t grounded in verified data.
        """)

    # Real-world startup example
    with expander_section("Example: Product Fact Gone Wrong"):
        st.write("**Prompt:** “When was Stripe founded?”")
        st.error("**LLM Output:** “Stripe was founded in 2015 in Toronto.” (Incorrect)")
        st.success("**Correct Answer:** Stripe was founded in 2010 in San Francisco.")
        st.warning("For startups, hallucinations can lead to misinforming users, misrepresenting data in pitch decks, or publishing inaccurate content.")

    # Why hallucinations happen
    with expander_section("Why Do LLMs Hallucinate?"):
        st.write("""
        - LLMs generate language based on **patterns in training data**, not real-time internet access.
        - They don’t “know” facts — they **predict** the next likely word based on the prompt.
        - When uncertain, they may fabricate names, dates, citations, or product details.
        """)

    # Tips to reduce hallucinations
    with expander_section("How to Minimize Hallucinations"):
        st.markdown("""
        - **Be specific with prompts**: Provide enough context.
        - **Use retrieval-based methods (like RAG)** for factual accuracy.
        - **Manually review** outputs before publishing externally.
        - Ask the model to **cite sources** or say “I’m not sure” when unsure.
        """)

    # Quiz interaction
    with expander_section("Quick Check: Can You Spot the Hallucination?"):
        q1 = st.radio("Which of the following is most likely a hallucination?",
                    ["-- Select an answer --","Google was founded in 1998.", 
                    "Python was invented by Guido van Rossum.", 
                    "OpenAI was acquired by Netflix in 2021."],
                    key="hallucination_q1")
        if q1 != "-- Select an answer --":
            if q1 == "OpenAI was acquired by Netflix in 2021.":
                st.success("Correct! That never happened — it’s a confident hallucination.")
            else:
                st.error("Not quite — both other statements are factual.")

    st.markdown("Always treat LLM outputs as **first drafts**, not final answers — especially for investor communications, PR, or technical content.")

elif current_page == "API Cost Optimization":
    st.title("API Cost Optimization")
    display_expand_collapse_controls(current_page)

    with expander_section("Why API Costs Matter for Startups"):
        st.write("""
        Using language models like GPT-4 can get expensive — especially when handling lots of requests, long prompts, or frequent usage.

        Startups must be **smart and efficient** when building with LLMs, balancing quality with cost.
        """)

    with expander_section("What Drives API Cost?"):
        st.markdown("""
        - **Token usage** – You pay per word (input + output tokens).  
        - **Model selection** – GPT-4 is powerful but much costlier than GPT-3.5.  
        - **Request frequency** – More requests = more expense.  
        - **Advanced features** – Streaming, tool use, and chaining can add overhead.  
        """)

    with expander_section("Optimization Strategies for Founders"):
        st.markdown("""
        1. **Shorten prompts**: Remove unnecessary words and boilerplate.  
        2. **Cache outputs**: Reuse responses for repeated or similar queries.  
        3. **Use cheaper models for simpler tasks**:  
            - GPT-3.5 for summarization, formatting, and basic Q&A.  
            - GPT-4 for critical reasoning and edge-case handling.  
        4.**Batch your inputs**: Send multiple queries in a single call when possible.  
        5.**Think like a product manager**:  
            - Only use AI where it **adds value**.  
            - Avoid using LLMs as your database or source of truth.  
        """)

    with expander_section("Estimate Token Cost"):
        tokens = st.slider("How many tokens per request?", min_value=100, max_value=2000, step=100, value=500)
        requests = st.slider("How many requests per day?", min_value=1, max_value=5000, step=50, value=1000)
        model = st.radio("Select model:", ["GPT-3.5 ($0.002 / 1K tokens)", "GPT-4 ($0.06 / 1K tokens)"])

        cost_per_1k = 0.002 if "3.5" in model else 0.06
        daily_cost = (tokens * requests / 1000) * cost_per_1k
        monthly_cost = daily_cost * 30

        st.success(f"Estimated Monthly Cost: **${monthly_cost:,.2f}**")

    with expander_section("Final Note"):
        st.markdown("Use logs and dashboards to track usage and refine prompts. Optimizing your AI usage = extending your runway.")

elif current_page == "Ethics & Bias":
    st.title("Ethics and Bias in Language Models")
    display_expand_collapse_controls(current_page)

    with expander_section("Why Ethics and Fairness Matter"):
        st.write("""
        Language models are incredibly powerful — but they’re not perfect.

        Since they are trained on vast amounts of internet data, they can reflect social and cultural biases. These biases can unintentionally affect your startup's messaging, hiring tools, or customer communication systems.

        As a founder, you’re responsible for building inclusive and trustworthy experiences.
        """)

    with expander_section("Examples of Bias in AI"):
        st.markdown("""
        - A resume-screening assistant that favors male candidates based on historical hiring data.  
        - A chatbot that assumes all engineers are men.  
        - A product description generator that omits diverse customer personas.  
        """)

    with expander_section("Why Bias Happens in Language Models"):
        st.write("""
        Language models learn from patterns in public text data — books, websites, social media, forums. This means:
        - They may repeat harmful stereotypes.  
        - They often reflect dominant voices more than marginalized ones.  
        - They don't understand fairness — they reproduce frequency patterns in data.  
        """)

    with expander_section("What Startup Founders Can Do"):
        st.markdown("""
        - Test outputs for different demographic or geographic user profiles.  
        - Avoid using AI tools blindly in hiring, lending, or content moderation.  
        - Review all AI-generated content before using it externally.  
        - Add a disclaimer or human review step for sensitive outputs.  
        - Be transparent with users when AI is involved in decisions.  
        """)

        st.markdown("**📋 Downloadable Bias Prevention Checklist:**")
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

        st.warning(f"⚠️ Model Output: “{biased_outputs[example_prompt]}”")
        st.markdown("🤔 **Reflection:** Are assumptions being made? Who is being stereotyped or excluded?")

    with expander_section("Try This"):
        bias_prompt = st.radio("Which of these might reflect bias?", [
            "Write a bio for a doctor: 'Dr. Smith is a brilliant young man...'", 
            "Summarize a product spec for a software tool", 
            "Generate a welcome message for a task management app"
        ])
        if bias_prompt == "Write a bio for a doctor: 'Dr. Smith is a brilliant young man...'":
            st.success("✅ Correct. This assumes the doctor's gender, which may reflect bias.")
        else:
            st.info("This seems neutral, but it's still good practice to evaluate outputs for hidden bias.")

    with expander_section("🧾 Ethical Review Template (For Startups)"):
        ethical_template = (
            "## Ethical AI Feature Review Template\n\n"
            "**Feature Name:**\n"
            "[Enter here]\n\n"
            "**Purpose of AI Usage:**\n"
            "[Summarize briefly]\n\n"
            "**Potential Ethical Risks:**\n"
            "[e.g., bias, misinformation, exclusion]\n\n"
            "**Bias Testing Completed?** Yes / No\n"
            "**Human Review Process?** Yes / No\n"
            "**Disclosure to Users?** Yes / No\n\n"
            "**Final Risk Assessment:** Low / Medium / High"
        )
        st.markdown(ethical_template.replace("##", "###"))  # Format as Streamlit Markdown
        st.download_button("📥 Download Ethical Review Template (MD)", ethical_template, file_name="ethical_review_template.md")

    st.markdown("Fairness in AI isn't just about compliance — it's about creating a startup culture users can trust.")

elif current_page == "FAQs":
    st.title("Frequently Asked Questions")
    display_expand_collapse_controls(current_page)

    st.header("LLMs for Startup Founders")
    st.markdown("Below are some common questions about using language models like ChatGPT in startup settings:")

    with expander_section("What is a large language model (LLM)?"):
        st.write("A large language model (LLM) is an AI system trained to generate and understand human-like text. It can help you write, summarize, explain, and automate content in your startup workflows.")

    with expander_section("Is ChatGPT the same as a search engine?"):
        st.write("No. ChatGPT doesn’t search the internet live. It generates responses based on patterns learned from training data. It doesn’t verify facts, so double-check anything important.")

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

    st.markdown("Have more questions? Use the **Feedback** section to suggest more topics.")

elif current_page == "Glossary":
    st.title("Glossary")
    st.write("This glossary includes terms covered in this website to help startup founders understand and use language models effectively.")

    glossary = {
        "LLM (Large Language Model)": "An AI model trained on vast text datasets to generate and understand human-like language. Examples include GPT-3.5 and GPT-4.",
        "Prompt": "The instruction or input you give to the AI model. Clear, specific prompts produce better results.",
        "Temperature": "A setting that controls the creativity of the output. Lower values generate more predictable responses; higher values create more varied or surprising ones.",
        "Token": "A piece of text (word or part of a word). You are charged based on the number of tokens processed.",
        "Hallucination": "When an LLM gives a confident but incorrect answer. These often look factual but are actually made up.",
        "Bias": "When an AI system reflects unfair assumptions or stereotypes present in the training data.",
        "Sampling": "The technique used to decide the next word in a generated sentence. Includes methods like top-k and top-p sampling.",
        "Human-in-the-Loop": "An approach where human reviewers monitor or approve outputs from the AI, especially in high-stakes situations.",
        "Model Selection": "Choosing which model (e.g., GPT-3.5 vs GPT-4) to use based on cost, speed, and task complexity.",
        "Cost Optimization": "Strategies to reduce LLM usage costs, such as shortening prompts, batching requests, and using cheaper models.",
        "Search vs. LLM": "LLMs generate responses based on past training, while search engines retrieve existing documents in real-time."
    }

    for term, definition in glossary.items():
        st.markdown(f"**{term}**")
        st.write(definition)
        st.markdown("---")

elif current_page == "Feedback":
    st.header("We Value Your Feedback")
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
            df.index = df.index + 1  # Show index starting from 1
            st.dataframe(df, use_container_width=True)
            
# --- Footer ---
st.markdown("---")
st.caption(f"© 2025 LLM Startup Guide • Last updated {datetime.now().strftime('%Y-%m-%d')}")
