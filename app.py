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

## 🧠 Sankofa Dashboard
if api_key:
    client = Groq(api_key=api_key)
    
    # Create the Tabs for the Dashboard
    tab1, tab2, tab3 = st.tabs(["🩺 Clinical Co-Pilot", "📦 Logistics Tracker", "💰 NHIS Calculator"])

    # --- TAB 1: CLINICAL CO-PILOT ---
    with tab1:
        st.subheader("AVHI: AI Virtual Health Intelligence")
        patient_case = st.text_area("Describe the case (Symptoms, age, weight):", placeholder="e.g. 5yo male, high fever, shivering, RDT positive")
        
        if st.button("Generate GHS Protocol"):
            with st.spinner("Consulting Ghana MoH & GHS Standards..."):
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system", 
                            "content": """You are AVHI, the AI core of Sankofa Health OS. 
                            Your knowledge is based STRICTLY on the Ghana Ministry of Health (MoH) 
                            Standard Treatment Guidelines (STG) and GHS clinical protocols.
                            
                            For every case, provide:
                            1. **Clinical Management**: Step-by-step per Ghana STG.
                            2. **Essential Meds**: List meds using Ghana NHIS generic names.
                            3. **G-DRG Code**: Provide the relevant Ghana Diagnosis-Related Group code for NHIS.
                            4. **Referral**: Criteria for referring from CHPS to District Hospital."""
                        },
                        {
                            "role": "user", 
                            "content": f"Based on Ghana MoH/GHS protocols, manage this case: {patient_case}"
                        }
                    ]
                )
                st.markdown(completion.choices[0].message.content)

    # --- TAB 2: LOGISTICS TRACKER ---
    with tab2:
        st.subheader("Inventory & Stock Management")
        col1, col2, col3 = st.columns(3)
        col1.metric("Artesunate (ACT)", "45", "-5")
        col2.metric("Amoxicillin", "120", "+12")
        col3.metric("RDT Kits", "12", "-20", delta_color="inverse")
        
        st.info("⚠️ Low Stock Alert: RDT Kits are below the safety threshold for this CHPS zone.")
        st.button("Request Re-stock from District")

    # --- TAB 3: NHIS CALCULATOR ---
    with tab3:
        st.subheader("Automated Claims Processing")
        diagnosis = st.selectbox("Select G-DRG Diagnosis", ["Malaria (Uncomplicated)", "Pneumonia", "Diarrheal Disease", "Hypertension"])
        
        # Current Ghana NHIS G-DRG approximate rates for 2026 demo
        rates = {"Malaria (Uncomplicated)": 48.00, "Pneumonia": 88.00, "Diarrheal Disease": 38.00, "Hypertension": 65.00}
        
        st.write(f"**Estimated NHIS Reimbursement:** GHS {rates[diagnosis]:.2f}")
        st.checkbox("Attach Digital Lab Result (RDT+)")
        if st.button("Submit Claim to NHIA"):
            st.success("Claim #SNK-992 queued for offline sync.")



else:
    st.warning("Please enter your Groq API Key in the sidebar to begin.")

