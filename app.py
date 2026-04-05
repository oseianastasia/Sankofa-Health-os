import streamlit as st
from groq import Groq

# 🏥 Branding
st.set_page_config(page_title="Sankofa Health OS", page_icon="🏥")
st.title("🏥 SANKOFA HEALTH OS")
st.markdown("*GHS Clinical Intelligence Prototype*")
# 🔑 Sidebar Setup
with st.sidebar:
    st.header("Settings")
    # This checks if the key exists in Secrets first
    api_key = st.secrets.get("GROQ_API_KEY") 
    
    # Optional: If you still want the text box as a backup
    user_key = st.text_input("Enter Groq API Key (Optional)", type="password")
    if user_key:
        api_key = user_key

    st.divider()
    st.info("Sankofa is optimized for rural CHPs")

# 🧠 Core Logic
if api_key:
    client = Groq(api_key=api_key)
    # ... the rest of your app code ...
else:
    st.warning("Please add your GROQ_API_KEY to Streamlit Secrets or enter it in the sidebar.")

