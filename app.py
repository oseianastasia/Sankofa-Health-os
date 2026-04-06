import streamlit as st
from groq import Groq

# 🎨 SANKOFA ELITE AESTHETIC CONFIG
st.set_page_config(page_title="Sankofa Health OS", page_icon="🛡️", layout="wide")

# Advanced CSS for a 2026 Professional Medical UI
st.markdown("""
    <style>
    /* Main Background & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F9FAFB; }

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #1F2937 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Neon Status Indicators */
    .status-online { color: #10B981; font-weight: bold; font-size: 12px; }
    
    /* Professional Card Styling */
    .med-card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border: 1px solid #F3F4F6;
        margin-bottom: 20px;
    }

    /* Active Patient Glow */
    .patient-hero {
        background: white;
        padding: 20px;
        border-radius: 20px;
        border-left: 6px solid #3B82F6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    }

    /* Action Buttons */
    .stButton>button {
        background: #3B82F6 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# 🔑 API & Data
api_key = st.secrets["GROQ_API_KEY"]
if api_key:
    client = Groq(api_key=api_key)

    # 🗄️ Real-time Data States
    if 'inventory' not in st.session_state:
        st.session_state.inventory = {"ACT": 42, "RDT": 8, "Amox": 120}
    if 'beds' not in st.session_state:
        st.session_state.beds = {"District Gen": 4, "Ridge": 0, "Korle Bu": 2}

    # 📱 PRO SIDEBAR
    with st.sidebar:
        st.markdown("<h1 style='color: white; font-size: 24px;'>SANKOFA <span style='color: #3B82F6;'>OS</span></h1>", unsafe_allow_html=True)
        st.markdown("<p class='status-online'>● SYSTEM ONLINE (CDSS v3.0)</p>", unsafe_allow_html=True)
        st.markdown("---")
        menu = st.radio("NAVIGATION", 
            ["📊 Dashboard", "🩺 Clinical Co-Pilot", "🚑 Emergency/No-Bed", "📦 Supply Chain", "💰 Claims Portal"])
        st.markdown("---")
        st.info("📍 Location: Central CHPS Zone B")

    # 👤 PATIENT HERO SECTION
    st.markdown("""
        <div class="patient-hero">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color: #6B7280; font-size: 12px; letter-spacing: 1px; font-weight: 700;">ACTIVE CASE</span>
                    <h2 style="margin: 0; color: #111827;">Ms. Ama Benson, 32F</h2>
                    <code style="color: #3B82F6;">UID: GH-2026-X892</code>
                </div>
                <div style="text-align: right;">
                    <span style="background: #FEE2E2; color: #EF4444; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">CRITICAL ALERT</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- ROUTING LOGIC ---

    if menu == "📊 Dashboard":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Vitals: BP", "142/90", "High", delta_color="inverse")
        with col2:
            st.metric("Vitals: SpO2", "96%", "Stable")
        with col3:
            st.metric("Temp", "38.5°C", "Fever", delta_color="inverse")
        
        st.markdown("### Clinical Alerts")
        st.warning("⚠️ Known Allergy: Penicillin G (Verified by GHS History)")
        st.error("🚨 Imminent Referral Risk: BP rising over 4-hour window.")

    elif menu == "🩺 Clinical Co-Pilot":
        st.markdown("### AVHI Clinical Intelligence")
        case_input = st.text_area("Live Consultation Notes", placeholder="Dictate or type patient symptoms here...", height=200)
        
        if st.button("Generate GHS Protocol"):
            with st.spinner("Analyzing against Ghana MoH Standard Treatment Guidelines..."):
                chat = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are AVHI. Ground all medical advice in Ghana Ministry of Health STG. Include G-DRG codes."},
                        {"role": "user", "content": case_input}
                    ]
                )
                st.success("Analysis Complete")
                st.markdown(chat.choices[0].message.content)

    elif menu == "🚑 Emergency/No-Bed":
        st.markdown("### Smart Referral Network")
        st.write("Live Bed Availability & Ambulance Dispatch")
        
        b1, b2, b3 = st.columns(3)
        b1.metric("District Gen", f"{st.session_state.beds['District Gen']} Beds")
        b2.metric("Ridge", "0 Beds", "FULL", delta_color="inverse")
        b3.metric("Korle Bu", f"{st.session_state.beds['Korle Bu']} Beds")

        if st.button("🚨 REQUEST IMMEDIATE NAS AMBULANCE"):
            st.error("Emergency Beacon Sent to National Ambulance Service.")

    elif menu == "📦 Supply Chain":
        st.markdown("### Automated Logistics")
        st.metric("Artesunate (ACT)", f"{st.session_state.inventory['ACT']} Units", "-2 Today")
        if st.button("Order Restock from District Store"):
            st.info("Logistics Request Queued.")

else:
    st.error("API Key missing. Check Streamlit Secrets.")




