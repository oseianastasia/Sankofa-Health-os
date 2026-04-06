 import streamlit as st
from groq import Groq

# 🎨 1. CONFIG & ELITE UI STYLING
st.set_page_config(page_title="Sankofa Health OS", page_icon="🇬🇭", layout="wide")

st.markdown("""
    <style>
    /* Dark Professional Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    [data-testid="stSidebar"] * { color: #f9fafb !important; }
    
    /* Main Background */
    .stApp { background-color: #f9fafb; }
    
    /* Professional Header Card */
    .main-header {
        background: white;
        padding: 24px;
        border-radius: 16px;
        border-left: 8px solid #3B82F6;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Global Button Styling */
    .stButton>button {
        border-radius: 10px;
        font-weight: 700;
        height: 3.5em;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# 🔑 2. API ACCESS
api_key = st.secrets["GROQ_API_KEY"]

if api_key:
    client = Groq(api_key=api_key)

    # 🗄️ 3. SYSTEM STATE (Persistent Data)
    if 'inventory' not in st.session_state:
        st.session_state.inventory = {"ACT (Adult)": 45, "RDT Kits": 12, "Amoxicillin": 80}
    if 'beds' not in st.session_state:
        st.session_state.beds = {"District Hospital A": 5, "Ridge Hospital": 0, "Municipal Clinic": 2}

    # 📱 4. VERTICAL NAVIGATION (Sidebar)
    with st.sidebar:
        st.markdown("<h2 style='letter-spacing: 1px;'>SANKOFA <span style='color: #3B82F6;'>OS</span></h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 11px; opacity: 0.7;'>v3.5 | GHS INTEGRATED SYSTEM</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Vertical Menu Selection
        menu = st.radio(
            "SYSTEM MODULES",
            ["🩺 Clinical Co-Pilot", "🚑 Referral & Beds", "📦 Logistics Tracker", "💰 NHIS Calculator"],
            index=0
        )
        
        st.markdown("---")
        st.success("● GHS Connection Active")
        st.info("📍 Node: Greater Accra Region")

    # 🏥 5. BRANDED HEADER (Universal & Professional)
    st.markdown("""
        <div class="main-header">
            <span style="color: #ef4444; font-size: 11px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase;">Ministry of Health • Ghana Health Service</span>
            <h1 style="margin: 5px 0; color: #111827; font-size: 26px;">🏥 SANKOFA HEALTH OS</h1>
            <p style="margin: 0; color: #3B82F6; font-size: 14px; font-weight: 500;">Standard Treatment Guidelines (STG) Intelligence Portal</p>
        </div>
    """, unsafe_allow_html=True)

    # --- 6. PAGE CONTENT LOGIC ---

    if menu == "🩺 Clinical Co-Pilot":
        st.subheader("Clinical Decision Support")
        st.caption("Grounded in MoH Standard Treatment Guidelines")
        
        patient_case = st.text_area("Patient History & Vitals:", height=200, 
                                    placeholder="e.g. 8yo Male, High Fever (39C), positive RDT, no danger signs...")

        if st.button("Generate GHS Protocol", type="primary"):
            with st.spinner("Analyzing against GHS/MoH Guidelines..."):
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": """You are AVHI, an AI clinical expert for Ghana. 
                        Your knowledge is strictly based on the Ghana Ministry of Health Standard Treatment Guidelines (STG).
                        Always provide: 1. Clinical Steps, 2. Generic Medications, 3. NHIS G-DRG Billing Code."""},
                        {"role": "user", "content": f"Manage this case per Ghana STG: {patient_case}"}
                    ]
                )
                st.markdown("### 📋 Recommended GHS Protocol")
                st.write(completion.choices[0].message.content)
                
                # Dynamic
