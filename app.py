import streamlit as st
import openai

st.set_page_config(page_title="CaseCoach AI", page_icon="💼", layout="wide")

# --- API Key ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "case_type" not in st.session_state:
    st.session_state.case_type = None

# --- GPT Call (simplified) ---
def chat_with_gpt(messages, model="gpt-4o-mini"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content

# --- Initial Prompt Template ---
def get_interviewer_prompt(case_type):
    return f"""
    You are an experienced consulting interviewer conducting a {case_type} case.
    Follow these steps:
    1. Present the problem statement like in a real case interview.
    2. Wait for the user's response. Ask probing questions based on their structure.
    3. Be strict but supportive. Do not give away answers.
    4. At the end, summarize their performance and rate them on:
       - Structure
       - Math
       - Creativity
       - Communication
    Keep your tone professional, like a McKinsey/Bain interviewer.
    """

# --- UI ---
st.title("💼 CaseCoach AI – Consulting Case Interview Practice")

# Case type selection
if st.session_state.case_type is None:
    st.session_state.case_type = st.selectbox(
        "Choose a case type to practice:", 
        ["Profitability", "Market Entry", "Growth Strategy", "M&A"]
    )
    if st.button("Start Case"):
    st.session_state.messages = [{"role": "system", "content": get_interviewer_prompt(st.session_state.case_type)}]
    # Get the initial case statement from GPT
    opening_statement = chat_with_gpt(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": opening_statement})
    st.rerun()
else:
    # Display previous messages
    for msg in st.session_state.messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if prompt := st.chat_input("Your response:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            full_response = chat_with_gpt(st.session_state.messages)
            st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Quick Drill Section
st.markdown("---")
st.subheader("🧠 Quick Mental Math Drill")
if st.button("Start Drill"):
    drill_prompt = "Give me 5 quick mental math questions relevant to consulting interviews with increasing difficulty."
    st.session_state.messages.append({"role": "user", "content": drill_prompt})
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        temperature=0.7
    )
    st.write(response.choices[0].message.content)
