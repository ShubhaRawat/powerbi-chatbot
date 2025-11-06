import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- CONFIG ---
genai.configure(api_key="YOUR_API_KEY_HERE")  
model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(
    page_title="Power BI AI Assistant",
    layout="wide",
    page_icon="💬"
)

# --- TITLE ---
st.markdown("<h2 style='text-align:center;'>💬 Power BI AI Assistant</h2>", unsafe_allow_html=True)

# --- SIDEBAR: Upload or Connect Data ---
st.sidebar.header("📊 Dataset Options")
uploaded_file = st.sidebar.file_uploader("Upload your Power BI CSV export", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ Data loaded successfully!")
else:
    st.sidebar.warning("Upload your Power BI dataset CSV to begin.")
    st.stop()

# --- CHAT MEMORY ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- USER INPUT ---
user_question = st.chat_input("Ask about your data...")

if user_question:
    with st.spinner("Analyzing your data..."):
        # Summarize dataset to make context lightweight
        summary = df.head(20).to_string(index=False)
        prompt = f"""
        You are a helpful data analysis assistant.
        The dataset is shown below:
        {summary}

        Question: {user_question}

        Answer clearly and concisely, using numeric evidence from the data if possible.
        """

        response = model.generate_content(prompt)
        answer = response.text

        # Save to session history
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

# --- DISPLAY CHAT ---
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])
