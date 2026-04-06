import streamlit as st
from groq import Groq

# 🎨 1. ELITE UI CONFIG (Must be first)
st.set_page_config(page_title="Sankofa Health OS", page_icon="🛡️", layout="wide")

# Professional Styling for 2026 Dashboard
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F9FAFB; }
    
    /* Sleek Card Styling */
    .stMetric { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #F3F4F6; }
    
    /* Professional Header */
    .main-header {
        background: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #3B82F6;
        margin-bottom: 25px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Buttons */
    .stButton>button { border-radius: 10px; font-weight: 600; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# 🔑 2. ACCESS SECRETS
api_key = st.secrets["GROQ_API_KEY"]

if api_key:
    client = Groq(api_key=api_key)

    # 🗄️ 3. SYSTEM STATE (Inventory & Beds)
    if 'inventory' not in st.session_state:
        st.session_state.inventory = {"ACT (Adult)": 45, "RDT Kits": 12, "Amoxicillin": 80}
    if 'beds' not in st.session_state:
        st.session_state.beds = {"District Hospital A": 5, "Ridge Hospital": 0, "Municipal Clinic": 2}

    # 🏥 4. CLEAN HEADER (No Double Title!)
    st.markdown("""
        <div class="main-header">
            <span style="color: #6B7280; font-size: 13px; font-weight: 700; letter-spacing: 1px;">GHANA HEALTH SERVICE • CLINICAL INTELLIGENCE</span>
            <h1 style="margin: 0; color: #111827; font-size: 28px;">SANKOFA HEALTH OS</h1>
            <p style="margin: 0; color: #3B82F6; font-weight: 500;">Resource Coordination & CDSS Portal</p>
        </div>
    """, unsafe_allow_html=True)

    # 📑 5. NAVIGATION TABS
    tab1, tab2, tab3, tab4 = st.tabs([
        "🩺 Clinical Co-Pilot", 
        "🚑 Referral & Beds", 
        "📦 Logistics Tracker", 
        "💰 NHIS Calculator"
    ])

    # --- TAB 1: CLINICAL CO-PILOT ---
    with tab1:
        st.subheader("AVHI Intelligence")
        st.info("🎤 Pro-Tip: Tap the mic on your keyboard to speak your diagnosis.")
        patient_case = st.text_area("Patient History & Vitals:", height=150, placeholder="e.g. 10yo Female, Temp 39C, RDT positive...")

        if st.button("Generate GHS Protocol", type="primary"):
            with st.spinner("Analyzing per Ghana MoH Guidelines..."):
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are AVHI. Base all advice on Ghana MoH Standard Treatment Guidelines. Provide Clinical Steps, Meds, and G-DRG Codes."},
                        {"role": "user", "content": f"Manage this case: {patient_case}"}
                    ]
                )
                st.markdown(completion.choices[0].message.content)
                
                if "Malaria" in completion.choices[0].message.content or "ACT" in completion.choices[0].message.content:
                    st.session_state.inventory["ACT (Adult)"] -= 1
                    st.session_state.inventory["RDT Kits"] -= 1
                    st.toast("Inventory Updated: -1 ACT, -1 RDT", icon="📦")

    # --- TAB 2: REFERRAL & BEDS (The No-Bed Syndrome Fix) ---
    with tab2:
        st.subheader("📍 Regional Coordination Hub")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚨 DISPATCH AMBULANCE (193)", use_container_width=True):
                st.error("NAS Alerted: Sending GPS & Patient Data.")
        
        with c2:
            target = st.selectbox("Destination Hospital", list(st.session_state.beds.keys()))
            if st.button(f"Transfer Data to {target}", use_container_width=True):
                if st.session_state.beds[target] > 0:
                    st.success(f"Bed Reserved at {target}!")
                    st.session_state.beds[target] -= 1
                else:
                    st.warning("No Beds Available. Try another facility.")

        st.divider()
        st.write("### Live Bed Map")
        m1, m2, m3 = st.columns(3)
        m1.metric("District Hospital A", f"{st.session_state.beds['District Hospital A']} Beds")
        m2.metric("Ridge Hospital", "0 Beds", "FULL", delta_color="inverse")
        m3.metric("Municipal Clinic", f"{st.session_state.beds['Municipal Clinic']} Beds")

    # --- TAB 3: LOGISTICS TRACKER ---
    with tab3:
        st.subheader("Supply Chain Monitor")
        l1, l2, l3 = st.columns(3)
        l1.metric("ACT (Adult)", st.session_state.inventory["ACT (Adult)"])
        l2.metric("RDT Kits", st.session_state.inventory["RDT Kits"])
        l3.metric("Amoxicillin", st.session_state.inventory["Amoxicillin"])

    # --- TAB 4: NHIS CALCULATOR ---
    with tab4:
        st.subheader("NHIS Claims Assistant")
        diag = st.selectbox("Diagnosis", ["Malaria", "Pneumonia", "Hypertension"])
        rates = {"Malaria": 48.50, "Pneumonia": 85.00, "Hypertension": 62.00}
        st.write(f"### Estimated Reimbursement: **GHS {rates[diag]:.2f}**")
        if st.button("Submit Claim"):
            st.success("Claim sent to NHIA Portal.")

else:
    st.error("Configure GROQ_API_KEY in Streamlit Secrets.")



