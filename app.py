import streamlit as st
from groq import Groq
import pandas as pd
import uuid
import plotly.express as px
from datetime import datetime

# 🎨 1. UI THEME
st.set_page_config(page_title="Sankofa OS", layout="wide", page_icon="🇬🇭")

st.markdown("""
    <style>
    /* 1. Sidebar Background */
    [data-testid="stSidebar"] { background-color: #0f172a; }
    
    /* 2. Text Colors */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    /* 3. GHS Badge (Dark Teal) */
    .status-badge { 
        background-color: #0d2121; border: 1px solid #134e4a; padding: 16px; 
        border-radius: 10px; margin-top: 10px; font-size: 14px; color: #ffffff !important; 
        font-weight: bold; text-align: left;
    }

    /* 4. Node Badge (Deep Navy) */
    .node-badge { 
        background-color: #1e293b; padding: 16px; border-radius: 10px; 
        margin-top: 12px; font-size: 14px; text-align: left; color: #ffffff !important;
    }

    /* 5. Header Styling */
    .ghs-header { 
        background: white; padding: 20px; border-radius: 15px; 
        border-left: 12px solid #ef4444; margin-bottom: 20px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); 
    }
    
    .stButton>button { width: 100%; border-radius: 10px; font-weight: 700; height: 3em; }
    </style>
    """, unsafe_allow_html=True)


# 🔑 2. SYSTEM CORE
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("SYSTEM ERROR: GROQ_API_KEY not found in Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# Global State Management
if 'inventory' not in st.session_state:
    st.session_state.inventory = {"ACT (Adult)": 45, "RDT Kits": 12, "Amoxicillin": 80, "Oxytocin": 15}
if 'session_data' not in st.session_state:
    st.session_state.session_data = "" 
if 'current_node' not in st.session_state:
    st.session_state.current_node = "Accra Central"

# 📍 LOCATION DATA
NODES = {
    "Accra Central": {"Ridge": 5, "37 Military": 0, "Korle-Bu": 2},
    "Kumasi Node": {"KATH": 1, "Kumasi South": 8, "SDA": 4},
    "Tamale Node": {"Tamale Teaching": 0, "Tamale West": 3, "Central": 6},
    "Ho Node": {"Ho Teaching": 4, "Trafalgar": 2, "Ho Municipal": 1}
}

# 📱 3. SIDEBAR
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
        <div class="node-badge">📍 Node: {st.session_state.current_node} | 2026-04-06</div>
    """, unsafe_allow_html=True)

# 🏥 4. HEADER
st.markdown("""<div class="ghs-header">
    <span style="color:#ef4444; font-weight:900; font-size:10px; letter-spacing:2px;">MINISTRY OF HEALTH • GHANA HEALTH SERVICE</span>
    <h2 style="margin:5px 0; color:#1e293b;">🏥 SANKOFA HEALTH OPERATING SYSTEM</h2>
</div>""", unsafe_allow_html=True)

# --- 5. MODULES ---

# 1. SCRIBE & CO-PILOT
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
        # Correctly using session_state.session_data
        st.session_state.session_data = st.text_area("Patient History (Type or Edit AI Notes):", value=st.session_state.session_data, height=150)
        st.markdown("### 💬 Clinical AI Co-Pilot")
        q = st.text_input("Ask Co-Pilot (e.g., 'What is the dosage for Malaria based on these notes?')")
        if q and st.session_state.session_data:
            res = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[
                {"role": "system", "content": "You are a Ghana Health Service Co-Pilot. Use patient notes and GHS Standard Treatment Guidelines (STG) to assist nurses."},
                {"role": "user", "content": f"Notes: {st.session_state.session_data}\nQuestion: {q}"}
            ])
            st.info(res.choices[0].message.content)

# 2. EMERGENCY, REFERRAL & BEDS
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

# 4. SURVEILLANCE
elif menu == "📈 Disease Surveillance":
    st.subheader("Epidemic Radar")
    df = pd.DataFrame({"Disease": ["Malaria", "Cholera", "Meningitis"], "Cases": [145, 3, 0]})
    st.plotly_chart(px.bar(df, x='Disease', y='Cases', color='Cases', color_continuous_scale="Reds"), use_container_width=True)
    if 3 in df.values: st.error(f"🚨 CLUSTER ALERT: Cholera detected at {st.session_state.current_node}.")

# 5.  # 5. PATIENT CARE (SANKOFA MULTILINGUAL CLOSED-LOOP)
elif menu == "👥 Patient Care & Adherence":
    st.subheader("🌍 Multilingual Community Follow-up")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📡 Initiate Monitoring")
        p_name = st.text_input("Patient Name", placeholder="e.g. Ama Mansa")
        p_type = st.selectbox("Monitoring Type", ["Maternal Postpartum", "Chronic Care", "Malaria Recovery"])
        # Language selection for the AI context
        target_lang = st.selectbox("Primary Language", ["Twi", "Hausa", "Ga", "Ewe", "Dagbani", "English"])
        chan = st.radio("Channel", ["💬 WhatsApp", "📩 SMS", "📞 AI Voice"])
        
        if st.button("Activate Multilingual Loop"):
            st.success(f"Protocol Active: Monitoring {p_name} in {target_lang}.")

    with col2:
        st.markdown("### 📥 Multilingual AI Analysis")
        st.info(f"AI is configured to interpret responses in **{target_lang}**.")
        
        # Simulated responses for demo purposes:
        # Twi: "Me ti pae me yie na me ho roro me" (My head hurts and I have chills)
        # Hausa: "Ina jin jiri kuma ina zubar da jini" (I feel dizzy and I am bleeding)
        raw_feedback = st.text_area("Simulated Incoming Message:", 
                                   placeholder=f"Enter text in {target_lang}...")
        
        if st.button("Translate & Analyze"):
            if raw_feedback:
                with st.spinner("Sankofa AI Analyzing Language & Sentiment..."):
                    # The AI logic to bridge the language gap
                    analysis_res = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": f"""
                                You are a medical translator for the Ghana Health Service. 
                                1. Translate the user's message from {target_lang} to English.
                                2. Identify if there are 'Danger Signs' (bleeding, severe pain, fever, dizziness).
                                3. Respond in JSON format: {{"translation": "...", "danger_detected": true/false}}
                            """},
                            {"role": "user", "content": raw_feedback}
                        ],
                        response_format={"type": "json_object"}
                    )
                    
                    import json
                    data = json.loads(analysis_res.choices[0].message.content)
                    
                    st.write(f"**English Translation:** {data['translation']}")
                    
                    if data['danger_detected']:
                        st.error(f"🚨 CRITICAL ALERT: Danger signs detected in {target_lang} response!")
                        st.markdown(f"""
                            <div style="background-color:#fee2e2; border:2px solid #ef4444; padding:15px; border-radius:10px; color:#b91c1c;">
                                <strong>Emergency Protocol:</strong> Immediate CHPS nurse intervention required for {p_name}.
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.success("AI Analysis: Patient appears stable.")
            else:
                st.warning("Please enter a message to analyze.")

    st.divider()
    st.markdown("### 📊 Regional Language Reach")
    lang_stats = pd.DataFrame({"Language": ["Twi", "English", "Hausa", "Ga", "Ewe"], "Active Users": [450, 310, 120, 85, 60]})
    st.bar_chart(lang_stats.set_index("Language"))


# 6. NHIS CLAIMS
elif menu == "💳 NHIS Claims Portal":
    st.subheader("NHIS Digital E-Claims")
    if st.session_state.session_data:
        st.write("**AI-Suggested G-DRG:** 4022 (Malaria)")
        if st.button("Submit Claim"):
            st.success(f"Claim #{uuid.uuid4().hex[:8].upper()} submitted.")
    else: st.warning("Record a consultation first.")
