import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="Semantic Cache LLM",
    page_icon="🧠"
)

st.title("🧠 Semantic Cache LLM")

question = st.text_input(
    "Ask a question:",
    placeholder="What is Artificial Intelligence?"
)

if st.button("Send"):

    if question:

        response = requests.post(
            API_URL,
            json={"prompt": question}
        )

        if response.status_code == 200:

            data = response.json()

            st.success("Response Received")

            st.write(data)

        else:
            st.error(
                f"Error {response.status_code}"
            )