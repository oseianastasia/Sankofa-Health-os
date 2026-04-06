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
        background: white; padding: 25px; border-radius: 15px;
        border-left: 10px solid #2563eb; margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .stButton>button { border-radius: 10px; font-weight: 700; height: 3.5em; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background-color: #2563eb; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 🔑 2. SYSTEM INITIALIZATION
api_key = st.secrets["GROQ_API_KEY"]
if api_key:
    client = Groq(api_key=api_key)

    # 🗄️ 3. NATIONAL HEALTH DATABASE
    if 'inventory' not in st.session_state:
        st.session_state.inventory = {"ACT (Adult)": 45, "RDT Kits": 12, "Amoxicillin": 80}
    if 'beds' not in st.session_state:
        st.session_state.beds = {"District Hosp A": 5, "Ridge": 0, "37 Military": 3}
    if 'active_session' not in st.session_state:
        st.session_state.active_session = None

    # 📱 4. NAVIGATION
    with st.sidebar:
        st.markdown("<h1 style='letter-spacing: 2px;'>SANKOFA <span style='color: #3B82F6;'>OS</span></h1>", unsafe_allow_html=True)
        st.caption("GHANA DIGITAL HEALTH INFRASTRUCTURE v6.0")
        st.markdown("---")
        menu = st.radio("SYSTEM MODULES", [
            "🎙️ Ambient Clinical Scribe", 
            "🚑 Emergency & Referral", 
            "📦 Smart Supply Chain",
            "📈 Disease Surveillance",
            "👥 Patient Care & Adherence"
        ])
        st.markdown("---")
        st.success("● GHS ENCRYPTED CONNECTION")
        st.info(f"📍 Node: Accra | {datetime.now().strftime('%Y-%m-%d')}")

    # 🏥 5. BRANDED HEADER
    st.markdown("""<div class="ghs-header">
        <span style="color: #ef4444; font-size: 11px; font-weight: 900; letter-spacing: 2px;">MINISTRY OF HEALTH • GHANA HEALTH SERVICE</span>
        <h1 style="margin: 8px 0; color: #1e2937; font-size: 26px;">🏥 SANKOFA HEALTH OPERATING SYSTEM</h1>
        <p style="margin: 0; color: #2563eb; font-weight: 600;">Ambient Intelligence & National Resource Gateway</p>
    </div>""", unsafe_allow_html=True)

    # --- 6. MODULES ---

    # MODULE: AMBIENT CLINICAL SCRIBE
    if menu == "🎙️ Ambient Clinical Scribe":
        st.subheader("Consultation Mode: Ambient Intelligence")
        st.info("The AI is listening to extract clinical data from your conversation in Twi, Ga, or English.")
        
        consultation_audio = st.audio_input("Start Consultation Recording")
        
        if consultation_audio:
            with st.spinner("Sankofa AI Scribe is extracting clinical facts..."):
                transcript = client.audio.transcriptions.create(
                    file=("live.wav", consultation_audio.read()), 
                    model="whisper-large-v3"
                ).text
                
                # AI EXTRACTION WITH LANGUAGE LOCK
                extraction = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a Ghanaian Medical Scribe. You MUST respond ONLY in English. Use Ghana Health Service terminology. Extract: Name, Age, Main Complaint, Duration, and Symptoms."
                        },
                        {
                            "role": "user", 
                            "content": f"Conversation Transcript: {transcript}"
                        }
                    ]
                )
                session_data = extraction.choices[0].message.content
                st.session_state.active_session = session_data

                st.success("✅ Session Auto-Populated")
                
                # Vertical Display for Mobile
                st.markdown("### 📋 Extracted Patient File")
                st.code(session_data, language="markdown")
                
                st.divider()
                
                st.markdown("### 🏥 Ghana STG Protocol")
                protocol = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a Ghana Health Service expert. Provide Standard Treatment Guidelines (STG) and NHIS G-DRG codes in English."
                        },
                        {
                            "role": "user", 
                            "content": session_data
                        }
                    ]
                )
                st.write(protocol.choices[0].message.content)
                
                if "Malaria" in session_data or "ACT" in protocol.choices[0].message.content:
                    st.session_state.inventory["ACT (Adult)"] -= 1
                    st.toast("Stock Auto-Deducted: -1 ACT", icon="💊")

    # MODULE: EMERGENCY & REFERRAL
    elif menu == "🚑 Emergency & Referral":
        st.subheader("Regional Resource Coordination")
        st.markdown('<a href="tel:193" style="text-decoration:none;"><div style="background:#ef4444; color:white; padding:20px; border-radius:10px; text-align:center; font-weight:bold; font-size:20px;">📞 CALL NAS 193</div></a>', unsafe_allow_html=True)
        
        st.divider()
        
        target = st.selectbox("Select Destination Hospital", ["Ridge Hospital", "37 Military", "Korle-Bu"])
        if st.button(f"Confirm Bed Availability & Refer"):
            if st.session_state.beds.get(target, 0) > 0:
                token = str(uuid.uuid4())[:8].upper()
                st.success(f"Bed Secured at {target}! Referral Token: {token}")
                st.session_state.beds[target] -= 1
            else:
                st.error(f"ALERT: {target} is FULL. Routing to next available node.")
        
        st.divider()
        st.write("### 🏥 Live Bed Radar")
        st.metric("Ridge Hospital", "0 Beds", "NO-BED ALERT", delta_color="inverse")
        st.metric("37 Military", f"{st.session_state.beds['37 Military']} Available")

    # MODULE: SMART SUPPLY CHAIN
    elif menu == "📦 Smart Supply Chain":
        st.subheader("Predictive Logistics")
        for item, qty in st.session_state.inventory.items():
            with st.container():
                st.write(f"**{item}** | Stock: {qty}")
                if qty < 20:
                    st.warning("LOW STOCK ALERT")
                    if st.button(f"Restock {item}"):
                        st.session_state.inventory[item] += 50
                        st.rerun()
                else:
                    st.success("Stock Level: Healthy")
                st.divider()

    # MODULE: DISEASE SURVEILLANCE
    elif menu == "📈 District Surveillance":
        st.subheader("Real-Time Epidemic Map")
        data = pd.DataFrame({"Disease": ["Malaria", "Cholera", "Yellow Fever"], "Cases": [145, 3, 0]})
        fig = px.bar(data, x='Disease', y='Cases', color='Disease')
        st.plotly_chart(fig, use_container_width=True)
        if data.loc[data['Disease'] == 'Cholera', 'Cases'].values[0] > 0:
            st.error("🚨 CHOLERA SIGNAL DETECTED. Alerts sent to District Health Director.")

    # MODULE: PATIENT CARE & ADHERENCE
    elif menu == "👥 Patient Care & Adherence":
        st.subheader("Chronic Care Monitoring")
        patients = [
            {"Name": "Ama Mansah", "Med": "Amlodipine", "Adherence": 92},
            {"Name": "Kwesi Appiah", "Med": "Metformin", "Adherence": 34}
        ]
        for p in patients:
            st.write(f"**{p['Name']}** - {p['Med']}")
            if p['Adherence'] < 50:
                st.error(f"Adherence: {p['Adherence']}% (Critical)")
                if st.button(f"Send Twi Reminder to {p['Name']}"):
                    st.toast("Voice Reminder Sent!")
            else:
                st.success(f"Adherence: {p['Adherence']}%")
            st.divider()

else:
    st.error("GROQ_API_KEY Missing. Add it to your Streamlit Secrets.")
