import streamlit as st
from groq import Groq
import pandas as pd
import uuid
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Sankofa Health OS", page_icon="🇬🇭", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0f172a; min-width: 300px; }
    [data-testid="stSidebar"] * { color: #f8fafc !important; }
    .stApp { background-color: #f1f5f9; }
    .ghs-header {
        background: white; padding: 20px; border-radius: 15px;
        border-left: 10px solid #2563eb; margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# API Setup
api_key = st.secrets["GROQ_API_KEY"]
if api_key:
    client = Groq(api_key=api_key)

    # Initialize session states
    if 'inventory' not in st.session_state:
        st.session_state.inventory = {"ACT (Adult)": 45, "RDT Kits": 12, "Amoxicillin": 80}
    if 'active_session' not in st.session_state:
        st.session_state.active_session = None

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("<h1>SANKOFA <span style='color: #3B82F6;'>OS</span></h1>", unsafe_allow_html=True)
        menu = st.radio("SELECT MODULE", [
            "🎙️ Ambient Scribe", 
            "🚑 Emergency Hotline", 
            "📦 Supply Chain",
            "📈 Disease Radar",
            "💳 NHIS Claims"
        ])

    # Header
    st.markdown("""<div class="ghs-header">
        <span style="color: #ef4444; font-size: 10px; font-weight: 900; letter-spacing: 2px;">MINISTRY OF HEALTH • GHANA</span>
        <h2 style="margin: 5px 0;">🏥 SANKOFA HEALTH OS</h2>
    </div>""", unsafe_allow_html=True)

    # --- Modules ---
    if menu == "🎙️ Ambient Scribe":
        st.subheader("Clinical Scribe")
        audio = st.audio_input("Record Consult")
        if audio:
            with st.spinner("Extracting..."):
                transcript = client.audio.transcriptions.create(file=("live.wav", audio.read()), model="whisper-large-v3").text
                res = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": "Extract clinical summary in English."},
                              {"role": "user", "content": transcript}]
                )
                st.session_state.active_session = res.choices[0].message.content
        if st.session_state.active_session:
            st.code(st.session_state.active_session)

    elif menu == "🚑 Emergency Hotline":
        st.subheader("Emergency Coordination")
        st.error("🚨 National Ambulance: 193")
        st.markdown('<a href="tel:193"><button style="width:100%; height:50px; background:red; color:white; border:none; border-radius:10px;">CALL 193</button></a>', unsafe_allow_html=True)
        st.divider()
        st.write("MoH Direct: 0302665651")
        st.write("GHS HQ: 0302661352")

    elif menu == "📦 Supply Chain":
        st.subheader("Inventory")
        st.table(pd.DataFrame(list(st.session_state.inventory.items()), columns=["Item", "Qty"]))

    elif menu == "📈 Disease Radar":
        st.subheader("Regional Surveillance")
        data = pd.DataFrame({"Disease": ["Malaria", "Cholera"], "Cases": [145, 3]})
        st.plotly_chart(px.bar(data, x='Disease', y='Cases'), use_container_width=True)

    elif menu == "💳 NHIS Claims":
        st.subheader("NHIS Portal")
        if st.session_state.active_session:
            st.success("Patient Record Ready")
            if st.button("Submit Claim"):
                st.balloons()
        else:
            st.warning("No session active.")
else:
    st.error("Missing GROQ_API_KEY in Secrets.")
 
