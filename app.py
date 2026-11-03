import streamlit as st
import requests

st.set_page_config(page_title="Nykaa AI Support", page_icon="🛍️")
st.title("🛍️ Nykaa Customer Support")

# Part 4: Session Memory initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box for the live demo
if prompt := st.chat_input("Ask about your order (e.g., Status of ORD-100001)..."):
    # Display user prompt in UI and save to memory
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send the request to your local FastAPI backend
    with st.chat_message("assistant"):
        try:
            res = requests.post("http://127.0.0.1:8000/api/support", json={"text": prompt})
            reply = res.json().get("agent_response", "Error reading response.")
            st.markdown(reply)
            
            # Save agent response to memory
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error("Could not connect. Ensure your FastAPI server is still running on port 8000.")