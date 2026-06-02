import streamlit as st
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

client = Groq()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role" : "system", "content" : "act like a teacher"}]

for message in st.session_state.messages:
    if message ["role"] != "system":
        with st.chat_message(message['role']):
            st.write(message["content"])

if user_input := st.chat_input("type here"):
    with st.chat_message("user"):
        st.write(user_input)

if user_input:
    st.session_state.messages.append({"role" : "user", "content" : user_input})

with st.chat_message("assistant"):
    response_container = st.empty()

    stream = client.chat.completions.create(
        model= "llama-3.3-70b-versatile",
        messages= st.session_state.messages,
        stream=True
    )

    assistance_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            assistance_response += chunk.choices[0].delta.content
            response_container.write(assistance_response)
st.session_state.messages.append({"role" : "assistant", "content" : assistance_response}) 




