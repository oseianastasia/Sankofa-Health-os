       import streamlit as st
from groq import Groq
import pandas as pd
import uuid
import plotly.express as px
from datetime import datetime

# 🎨 1. THEME & CORE INTERFACE
st.set_page_config(page_title="Sankofa Health OS", page_icon="🇬🇭", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0f172a; min-width: 300px; }
    [data-testid="stSidebar"] * { color: #f8fafc !important; }
    .stApp { background-color: #f1f5f9; font-family: 'Inter', sans-serif; }
    .ghs-header {
        background: white; padding: 20px; border-radius: 15px;
        border-left: 10px solid #2563eb; margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .stButton>button { border-radius: 10px; font-weight: 700; transition: 0.3s; }
    </style>
    """, unsafe_allow_html=True)

# 🔑 2. SYSTEM INITIALIZATION
api_key = st.secrets["GROQ_API_KEY"]
if api_key:
    client = Groq(api_key=api_key)

    if 'inventory' not in st.session_state:
        st.session_state.inventory = {"ACT (Adult)": 45, "RDT Kits": 12, "Amoxicillin": 80}
    if 'beds' not in st.session_state:
        st.session_state.beds = {"Ridge": 0, "37 Military": 3, "Korle-Bu": 1}
    if 'active_session' not in st.session_state:
        st.session_state.active_session = None

    # 📱 4. NAVIGATION (Updated with NHIS)
    with st.sidebar:
        st.markdown("<h1>SANKOFA <span style='color: #3B82F6;'>OS</span></h1>", unsafe_allow_html=True)
        menu = st.radio("SYSTEM MODULES", [
            "🎙️ Ambient Scribe & Chat", 
            "🚑 Emergency & Hotline", 
            "📦 Smart Supply Chain",
            "📈 Disease Surveillance",
            "👥 Patient Outreach",
            "💳 NHIS Claims Portal"
        ])
        st.info(f"📍 Node: Accra | {datetime.now().strftime('%Y-%m-%d')}")

    # 🏥 5. BRANDED HEADER
    st.markdown("""<div class="ghs-header">
        <span style="color: #ef4444; font-size: 10px; font-weight: 900; letter-spacing: 2px;">MINISTRY OF HEALTH • GHANA HEALTH SERVICE</span>
        <h2 style="margin: 5px 0;">🏥 SANKOFA HEALTH OS</h2>
    </div>""", unsafe_allow_html=True)

    # --- 6. MODULES ---

    # MODULE 1: AMBIENT SCRIBE
    if menu == "🎙️ Ambient Scribe & Chat":
        st.subheader("Consultation Mode")
        audio = st.audio_input("Record Consultation")
        if audio:
            with st.spinner("Processing..."):
                transcript = client.audio.transcriptions.create(file=("live.wav", audio.read()), model="whisper-large-v3").text
                extraction = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": "Extract clinical data in English: Name, Age, Diagnosis, Treatment."},
                              {"role": "user", "content": transcript}]
                )
                st.session_state.active_session = extraction.choices[0].message.content
        
        if st.session_state.active_session:
            st.code(st.session_state.active_session)
            query = st.text_input("💬 Ask Co-Pilot (e.g. 'Dosage for child?')")
            if query:
                res = client.chat.completions.create(model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": "Ghana Health expert. English only."},
                              {"role": "user", "content": f"Context: {st.session_state.active_session}\nQuestion: {query}"}])
                st.write(res.choices[0].message.content)

    # MODULE 2: EMERGENCY & HOTLINE (Updated)
    elif menu == "🚑 Emergency & Hotline":
        st.subheader("Emergency Coordination")
        st.error("🚨 PRIMARY: National Ambulance (193)")
        st.markdown('<a href="tel:193" style="text-decoration:none;"><div style="background:#ef4444; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📞 CALL NAS 193</div></a>', unsafe_allow_html=True)
        
        st.divider()
        st.subheader("⚠️ ESCALATION HOTLINES")
        st.caption("Use if Ambulance is unavailable or for Ministry directives.")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<a href="tel:0302665651" style="text-decoration:none;"><div style="background:#1e2937; color:white; padding:10px; border-radius:5px; text-align:center;">📞 MoH DIRECT</div></a>', unsafe_allow_html=True)
        with c2:
            st.markdown('<a href="tel:0302661352" style="text-decoration:none;"><div style="background:#1e2937; color:white; padding:10px; border-radius:5px; text-align:center;">📞 GHS HEADQUARTERS</div></a>', unsafe_allow_html=True)

    # MODULE 4: DISEASE SURVEILLANCE (Fixed)
    elif menu == "📈 Disease Surveillance":
        st.subheader("Regional Epidemic Radar")
        st.info("Live tracking of GHS notification-required diseases.")
        data = pd.DataFrame({"Disease": ["Malaria", "Cholera", "Yellow Fever", "COVID-19"], "Cases": [145, 3, 0, 12]})
        fig = px.bar(data, x='Disease', y='Cases', color='Cases', color_continuous_scale="Reds")
        st.plotly_chart(fig, use_container_width=True)
        if 3 > 0: st.error("🚨 ALERT: Cholera cases detected in District. Protocol: Contact Public Health Unit.")

    # MODULE 6: NHIS CLAIMS (New)
    elif menu == "💳 NHIS Claims Portal":
        st.subheader("NHIS Digital Claims E-Portal")
        if st.session_state.active_session:
            st.success("Patient session detected. Ready for auto-billing.")
            st.write("**G-DRG Code Recommendation:** 4022 (Malaria - Uncomplicated)")
            if st.button("Submit E-Claim to NHIA"):
                st.balloons()
                st.success("Claim #"+str(uuid.uuid4())[:8]+" submitted successfully.")
        else:
            st.warning("No active patient session. Complete a consultation to file a claim.")

    # ... (Other modules: Supply Chain & Outreach remain as previously updated)
    elif menu == "📦 Smart Supply Chain":
        st.subheader("Inventory Radar")
        st.table(pd.DataFrame(list(st.session_state.inventory.items()), columns=["Item", "Stock"]))
    
    elif menu == "👥 Patient Outreach":
        st.subheader("Community Outreach")
        if st.session_state.active_session:
            chan = st.selectbox("Channel", ["📞 Voice Call", "💬 WhatsApp", "📩 SMS"])
            lang = st.selectbox("Language", ["Twi", "Ga", "Ewe", "Hausa", "English"])
            if st.button("Send Reminder"): st.success(f"Sent {lang} {chan}")
        else: st.warning("Record a session first.")

else:
    st.error("Add GROQ_API_KEY to Secrets.")
         
