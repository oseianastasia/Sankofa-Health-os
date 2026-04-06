import streamlit as st
from groq import Groq

# 🏥 Branding
st.set_page_config(page_title="Sankofa Health OS", page_icon="🏥")
st.title("🏥 SANKOFA HEALTH OS")
st.markdown("*GHS Clinical Intelligence Prototype*")

# 🔑 Sidebar Setup
with st.sidebar:
    st.header("Settings")
    # This line below is the "Magic" that connects to your Secrets
    api_key = st.secrets["GROQ_API_KEY"] 
    st.divider()
    st.info("Sankofa is optimized for rural CHPs")

##import streamlit as st
from groq import Groq

# 🎨 Custom Aesthetic Styling
st.set_page_config(page_title="Sankofa Health OS", page_icon="🩺", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    .status-card { padding: 20px; border-radius: 10px; color: white; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 🔑 Access Secrets
api_key = st.secrets["GROQ_API_KEY"]

if api_key:
    client = Groq(api_key=api_key)

    # 🗄️ System "Database" (Session State)
    if 'inventory' not in st.session_state:
        st.session_state.inventory = {"ACT (Adult)": 45, "RDT Kits": 12, "Amoxicillin": 80}
    if 'beds' not in st.session_state:
        st.session_state.beds = {"District Hospital A": 5, "Ridge Hospital": 0, "Municipal Clinic": 2}

    # 🏥 Header Section
    st.title("🏥 SANKOFA HEALTH OS")
    st.markdown("### *GHS Clinical Intelligence & Resource Coordination*")
    st.divider()

    # 📑 The Dashboard Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🩺 Clinical Co-Pilot", 
        "🚑 Referral & Beds", 
        "📦 Logistics Tracker", 
        "💰 NHIS Calculator"
    ])

    # --- TAB 1: CLINICAL CO-PILOT (The Brain) ---
    with tab1:
        st.subheader("AVHI: AI Virtual Health Intelligence")
        st.info("💡 Pro-Tip: Use your mobile keyboard's 🎤 icon to dictate in Twi or English.")
        
        patient_case = st.text_area("Patient History / Vitals:", height=150, placeholder="e.g. 5yo Male, Fever 39C, RDT positive, coughing...")

        if st.button("Generate GHS Protocol", type="primary"):
            with st.spinner("Consulting Ghana MoH Standard Treatment Guidelines..."):
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": """You are AVHI. Your knowledge is based STRICTLY on the Ghana MoH STG. 
                        Always provide: 1. Clinical Steps (GHS), 2. Essential Meds (NHIS Generic), 3. G-DRG Code."""},
                        {"role": "user", "content": f"Manage this case per Ghana GHS/MoH protocols: {patient_case}"}
                    ]
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                
                # Auto-deduct stock if Malaria is treated
                if "Malaria" in response or "ACT" in response:
                    st.session_state.inventory["ACT (Adult)"] -= 1
                    st.session_state.inventory["RDT Kits"] -= 1
                    st.toast("Inventory Auto-Updated", icon="📦")

    # --- TAB 2: REFERRAL & BEDS (No-Bed Syndrome Fix) ---
    with tab2:
        st.subheader("📍 Emergency Coordination")
        
        col_nas, col_handover = st.columns(2)
        with col_nas:
            if st.button("🚨 DISPATCH AMBULANCE (193)"):
                st.error("Connecting to National Ambulance Service... Data Sent.")
        
        with col_handover:
            target = st.selectbox("Destination Hospital", list(st.session_state.beds.keys()))
            if st.button(f"Transfer Patient File to {target}"):
                if st.session_state.beds[target] > 0:
                    st.success(f"Bed Reserved at {target}!")
                    st.session_state.beds[target] -= 1
                else:
                    st.warning("No Beds Available at selected facility.")

        st.markdown("---")
        st.write("### Live Regional Bed Map")
        c1, c2, c3 = st.columns(3)
        for i, (hosp, count) in enumerate(st.session_state.beds.items()):
            cols = [c1, c2, c3]
            cols[i].metric(hosp, f"{count} Beds", delta="Available" if count > 0 else "FULL", delta_color="normal" if count > 0 else "inverse")

    # --- TAB 3: LOGISTICS TRACKER (Supply Chain) ---
    with tab3:
        st.subheader("Inventory Management")
        l1, l2, l3 = st.columns(3)
        l1.metric("ACT (Adult)", st.session_state.inventory["ACT (Adult)"])
        l2.metric("RDT Kits", st.session_state.inventory["RDT Kits"], delta="-2 Today")
        l3.metric("Amoxicillin", st.session_state.inventory["Amoxicillin"])
        
        if st.button("Request Emergency Re-stock"):
            st.info("Re-stock request sent to District Medical Store.")

    # --- TAB 4: NHIS CALCULATOR (Revenue) ---
    with tab4:
        st.subheader("NHIS Claims Assistant")
        diagnosis = st.selectbox("Select Confirmed Diagnosis", ["Malaria", "Pneumonia", "Hypertension", "Anemia"])
        rates = {"Malaria": 48.50, "Pneumonia": 85.00, "Hypertension": 62.00, "Anemia": 55.00}
        
        st.write(f"### Estimated Reimbursement: **GHS {rates[diagnosis]:.2f}**")
        if st.button("Submit Digital Claim"):
            st.success("Claim submitted to NHIA portal successfully.")

else:
    st.error("Please configure your GROQ_API_KEY in Streamlit Secrets.")




