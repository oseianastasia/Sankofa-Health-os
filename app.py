import streamlit as st
from groq import Groq

# 🏥 Branding
st.set_page_config(page_title="Sankofa Health OS", page_icon="🏥")
st.title("🏥 SANKOFA HEALTH OS")
st.markdown("*GHS Clinical Intelligence Prototype*")

# 🔑 Sidebar Setup
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Groq API Key", type="password")
    st.divider()
    st.info("Sankofa is optimized for rural CHPS compounds.")

# 🧠 Core Logic
if api_key:
    client = Groq(api_key=api_key)
    st.subheader("🩺 Clinical Co-Pilot")
    patient_case = st.text_area("Describe the case (Symptoms, age, weight):")

    if st.button("Generate GHS Protocol"):
        with st.spinner("Consulting GHS Standard Treatment Guidelines..."):
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are the Sankofa Co-Pilot. Use Ghana Health Service protocols. Provide triage, 15kg-based dosage for malaria/fever, and a Twi summary for the patient."},
                    {"role": "user", "content": patient_case}
                ]
            )
            st.success("Protocol Ready!")
            st.write(completion.choices[0].message.content)
else:
    st.warning("Please enter your Groq API Key in the sidebar to begin.")
