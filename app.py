import streamlit as st
import pandas as pd
from crew_setup import handle_query

# Page Configuration
st.set_page_config(
    page_title="Multi-Agent Client Query Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Professional Heading
st.markdown(
    "<h2 style='text-align: center; color: #1f2937;'>🤖 Multi-Agent Client Query Chatbot</h2>",
    unsafe_allow_html=True
)

# Sidebar with FAQ Upload & Sample Questions
st.sidebar.header("📂 FAQ Upload & Sample Questions")
uploaded_file = st.sidebar.file_uploader("Upload FAQ CSV", type=["csv"])

# Sample Questions
sample_questions = [
    # FAQ-based
    "How can I reset my password?",
    "Where can I download the latest reports?",
    # LLM-based (General AI queries)
    "How does your company handle GDPR compliance?",
    "Can you suggest ways to improve my account security?",
    "Is there a way to automate recurring tasks within the platform?"
]

st.sidebar.subheader("💡 Sample Questions")
for question in sample_questions:
    if st.sidebar.button(question):
        st.session_state.user_input = question

# Load FAQ Dataset
faq_df = pd.read_csv(uploaded_file) if uploaded_file else None

# Initialize Chat History
if "history" not in st.session_state:
    st.session_state.history = []

# Input Area for User Query
st.subheader("🔍 Ask Your Question")
user_input = st.text_input("Enter your query:", key="user_input")

# Query Handling via CrewAI Agents
if user_input and faq_df is not None:
    with st.spinner("Processing your query..."):
        response = handle_query(user_input, faq_df)
        st.session_state.history.append({"user": user_input, "bot": response})
elif user_input:
    st.warning("⚠️ Please upload a valid FAQ CSV file first.")

# Chat History Display
if st.session_state.history:
    st.subheader("🗂️ Conversation History")
    for chat in st.session_state.history:
        st.markdown(f"**🧑 You:** {chat['user']}")
        st.markdown(f"**🤖 Bot:** {chat['bot']}")
        st.markdown("---")

# Styling for Professional Look
st.markdown(
    """
    <style>
    .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f9fafb;
    }
    .css-18e3th9 { padding: 2rem; }
    .css-1d391kg {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True
)
