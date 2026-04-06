import streamlit as st
from groq import Groq
import pandas as pd
import uuid
import plotly.express as px
from datetime import datetime

# 🎨 1. UI THEME (EXACT TEMPLATE MATCH)
st.set_page_config(page_title="Sankofa OS", layout="wide", page_icon="🇬🇭")

st.markdown("""
    <style>
    /* Dark Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #0f172a; min-width: 350px; }
    [data-testid="stSidebar"] * { color: #cbd5e1 !important; }
    
    /* GHS Status Badges */
    .status-badge { 
        background-color: #162e35; border: 1px solid #1e40af; padding: 12px; 
        border-radius: 8px; margin-top: 10px; font-size: 13px; color: #93c5fd !important; 
        font-weight: bold; text-align: center;
    }
    .node-badge { 
        background-color: #1e293b; padding: 12px; border-radius: 8px; 
        margin-top: 10px; font-size: 13px; text-align: center; color: #f8fafc !important;
    }

    /* Branded Ministry Header */
    .ghs-header { 
        background: white; padding: 20px; border-radius: 15px; 
        border-left: 12px solid #ef4444; margin-bottom: 20px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); 
    }
    
    .stButton>button { width: 100%; border-radius: 10px; font-weight: 700; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# 🔑 2. SYSTEM CORE & STATE
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("SYSTEM ERROR: GROQ_API_KEY not found in Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# Global State (Persistent History & Inventory)
if 'inventory' not in st.session_state:
    st.session_state.inventory = {"ACT (Adult)": 45, "RDT Kits": 12, "Amoxicillin": 80, "Oxytocin": 15}
if 'session_data' not in st.session_state:
    st.session_data = "" 
if 'current_node' not in st.session_state:
    st.session_state.current_node = "Accra Central"

# 📍 LOCATION-BASED REFERRAL & BED DATA
NODES = {
    "Accra Central": {"Ridge": 5, "37 Military": 0, "Korle-Bu": 2},
    "Kumasi Node": {"KATH": 1, "Kumasi South": 8, "SDA": 4},
    "Tamale Node": {"Tamale Teaching": 0, "Tamale West": 3, "Central": 6},
    "Ho Node": {"Ho Teaching": 4, "Trafalgar": 2, "Ho Municipal": 1}
}

# 📱 3. SIDEBAR (MATCHING YOUR TEMPLATE)
with st.sidebar:
    st.markdown("<h2 style='letter-spacing:1px;'>SANKOFA OS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px; opacity:0.8;'>GHANA DIGITAL HEALTH INFRASTRUCTURE<br>v6.0</p>", unsafe_allow_html=True)
    st.divider()
    
    st.session_state.current_node = st.selectbox("📍 Set Facility Location", list(NODES.keys()))
    
    st.markdown("<p style='font-size:12px; font-weight:bold; color:#64748b;'>SYSTEM MODULES</p>", unsafe_allow_html=True)
    menu = st.radio("Select", [
        "🎙️ Ambient Clinical Scribe", 
        "🚑 Emergency & Referral", 
        "📦 Smart Supply Chain",
        "📈 Disease Surveillance",
        "👥 Patient Care & Adherence",
        "💳 NHIS Claims Portal"
    ], label_visibility="collapsed")
    
    st.markdown(f"""
        <div class="status-badge">● GHS ENCRYPTED CONNECTION</div>
        <div class="node-badge">📍 Node: {st.session_state.current_node} | {datetime.now().strftime('%Y-%m-%d')}</div>
    """, unsafe_allow_html=True)

# 🏥 4. BRANDED HEADER
st.markdown("""<div class="ghs-header">
    <span style="color:#ef4444; font-weight:900; font-size:10px; letter-spacing:2px;">MINISTRY OF HEALTH • GHANA HEALTH SERVICE</span>
    <h2 style="margin:5px 0; color:#1e293b;">🏥 SANKOFA HEALTH OPERATING SYSTEM</h2>
</div>""", unsafe_allow_html=True)

# --- 5. MODULES ---

# 1. SCRIBE & NURSE CO-PILOT
if menu == "🎙️ Ambient Clinical Scribe":
    st.subheader("Clinical Gateway (Voice + Manual)")
    t1, t2 = st.tabs(["🎤 Voice Scribe", "⌨️ Manual Entry & AI Co-Pilot"])
    with t1:
        audio = st.audio_input("Record Patient Interaction")
        if audio:
            with st.spinner("AI Transcribing..."):
                transcript = client.audio.transcriptions.create(file=("live.wav", audio.read()), model="whisper-large-v3").text
                st.session_state.session_data = transcript
    with t2:
        st.session_state.session_data = st.text_area("Patient History (Type or Edit AI Notes):", value=st.session_state.session_data, height=150)
        st.markdown("### 💬 Clinical AI Co-Pilot")
        q = st.text_input("Ask Co-Pilot (e.g., 'What is the dosage for Malaria based on these notes?')")
        if q and st.session_state.session_data:
            res = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[
                {"role": "system", "content": "You are a Ghana Health Service Co-Pilot. Use patient notes and GHS Standard Treatment Guidelines (STG) to assist nurses."},
                {"role": "user", "content": f"Notes: {st.session_state.session_data}\nQuestion: {q}"}
            ])
            st.info(res.choices[0].message.content)

# 2. EMERGENCY, REFERRAL & BED TRACKING
elif menu == "🚑 Emergency & Referral":
    st.subheader("Critical Coordination & Bed Tracking")
    st.error("🚨 NATIONAL AMBULANCE SERVICE: 193")
    st.markdown(f'<a href="tel:193"><button style="background:red; color:white;">📞 CALL NAS 193</button></a>', unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🛏️ Live Facility Occupancy")
    current_beds = NODES[st.session_state.current_node]
    cols = st.columns(len(current_beds))
    for i, (hosp, count) in enumerate(current_beds.items()):
        with cols[i]:
            st.metric(label=hosp, value=f"{count} Beds", delta="🟢" if count > 0 else "🔴")

    st.divider()
    st.subheader("📤 Secure Digital Referral")
    target = st.selectbox("Select Destination", list(current_beds.keys()))
    if current_beds[target] == 0:
        st.warning(f"⚠️ {target} is at FULL CAPACITY.")
    
    if st.button("Transfer History & Secure Bed"):
        if st.session_state.session_data:
            st.success(f"History Sent to {target}! ID: SNK-{uuid.uuid4().hex[:6].upper()}")
        else: st.warning("Record patient notes in Scribe first.")

    st.divider()
    st.subheader("⚠️ Escalation Lines")
    c1, c2 = st.columns(2)
    with c1: st.markdown('[📞 MoH Direct: 0302665651](tel:0302665651)', unsafe_allow_html=True)
    with c2: st.markdown('[📞 GHS HQ: 0302661352](tel:0302661352)', unsafe_allow_html=True)

# 3. SUPPLY CHAIN
elif menu == "📦 Smart Supply Chain":
    st.subheader("Inventory Tracker")
    st.table(pd.DataFrame(list(st.session_state.inventory.items()), columns=["Item", "Stock"]))
    if st.button("Request Emergency Restock"):
        st.success("Requisition sent to Regional Medical Store.")

# 4. DISEASE SURVEILLANCE
elif menu == "📈 Disease Surveillance":
    st.subheader("Epidemic Radar")
    df = pd.DataFrame({"Disease": ["Malaria", "Cholera", "Meningitis"], "Cases": [145, 3, 0]})
    st.plotly_chart(px.bar(df, x='Disease', y='Cases', color='Cases', color_continuous_scale="Reds"), use_container_width=True)
    if 3 in df.values: st.error(f"🚨 CLUSTER ALERT: Cholera detected at {st.session_state.current_node}.")

# 5. PATIENT CARE (SMS/WHATSAPP)
elif menu == "👥 Patient Care & Adherence":
    st.subheader("Community Follow-up")
    p_name = st.text_input("Patient Name")
    lang = st.selectbox("Language", ["Twi", "Ga", "Ewe", "Hausa", "English"])
    chan = st.radio("Channel", ["💬 WhatsApp", "📩 SMS", "📞 Voice"])
    if st.button("Activate Follow-up"):
        st.success(f"Monitoring {p_name} in {lang} via {chan}.")

# 6. NHIS CLAIMS (BILLING)
elif menu == "💳 NHIS Claims Portal":
    st.subheader("NHIS Digital E-Claims")
    if st.session_state.session_data:
        st.write("**AI-Suggested G-DRG:** 4022 (Malaria)")
        if st.button("Submit Claim"):
            st.success(f"Claim #{uuid.uuid4().hex[:8].upper()} submitted.")
    else: st.warning("Record a consultation first.")
