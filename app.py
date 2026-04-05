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


# 🧠 Core Logic
if api_key:
    client = Groq(api_key=api_key)
    st.subheader("🩺 Clinical Co-Pilot")
    patient_case = st.text_area("Describe the case (Symptoms, age, weight):")

    if st.button("Generate GHS Protocol"):
        with st.spinner("Consulting GHS Standard Treatment Guidelines..."):
                        completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a GHS clinical protocol expert."},
                    {"role": "user", "content": f"Provide GHS protocol for: {patient_case}"}
                ]
            )
            st.success("Protocol Ready!")
            st.write(completion.choices[0].message.content)

else:
    st.warning("Please enter your Groq API Key in the sidebar to begin.")

