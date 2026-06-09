import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        st.error("Groq API Key not configured")
        st.stop()

client = Groq(api_key=api_key)

st.set_page_config(
    page_title="Email Tone Rewriter",
    page_icon="📧",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
background:#0e1117;
}

.main-title{
text-align:center;
font-size:48px;
font-weight:bold;
color:white;
}

.sub-title{
text-align:center;
color:#9ca3af;
margin-bottom:30px;
}

.stButton > button{
width:100%;
height:50px;
font-size:18px;
font-weight:bold;
border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
'<p class="main-title">📧 Email Tone Rewriter</p>',
unsafe_allow_html=True
)

st.markdown(
'<p class="sub-title">Rewrite Emails with Professional AI Assistance</p>',
unsafe_allow_html=True
)

col1, col2 = st.columns([3,1])

with col1:
    email_text = st.text_area(
        "Paste Your Email",
        height=300,
        placeholder="Paste your email here..."
    )

with col2:
    tone = st.selectbox(
        "Select Tone",
        [
            "Professional",
            "Formal",
            "Friendly",
            "Polite",
            "Executive",
            "Confident"
        ]
    )

if st.button("🚀 Rewrite Email"):

    if not email_text.strip():
        st.warning("Please enter an email.")
        st.stop()

    prompt = f"""
Rewrite the following email.

Tone: {tone}

Provide:

1. Suggested Subject
2. Rewritten Email
3. Grammar Improvements

Email:

{email_text}

Make the response natural and human.
"""

    with st.spinner("Rewriting Email..."):

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],
            temperature=0.5
        )

        rewritten = response.choices[0].message.content

    st.success("Email Rewritten Successfully")

    st.markdown(rewritten)

    st.download_button(
        "📥 Download Email",
        rewritten,
        file_name="rewritten_email.txt",
        mime="text/plain"
    )