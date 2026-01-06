from ollama import chat
import streamlit as st

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Ollama Chatbot",
    page_icon="🦙",
    layout="centered"
)

# -------------------- HEADER --------------------
st.markdown(
    """
    <h1 style='text-align: center;'>🦙 Ollama Chatbot</h1>
    <p style='text-align: center; color: gray;'>
    Local LLM powered by Ollama & Streamlit
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.header("⚙️ Settings")

    model = st.selectbox(
        "Choose Model",
        ["gemma2:2b", "llama3", "mistral"],
        index=0
    )

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption("💡 Runs 100% locally using Ollama")

# -------------------- SESSION STATE --------------------
if "ollama_model" not in st.session_state:
    st.session_state["ollama_model"] = model

st.session_state["ollama_model"] = model

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------- CHAT HISTORY --------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------- USER INPUT --------------------
if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        def generate_response():
            stream = chat(
                model=st.session_state["ollama_model"],
                messages=st.session_state.messages,
                stream=True,
            )
            for chunk in stream:
                if chunk["message"]["content"]:
                    yield chunk["message"]["content"]

        response = st.write_stream(generate_response())

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

# -------------------- FOOTER --------------------
st.markdown(
    """
    <hr>
    <p style='text-align:center; color:gray; font-size: 14px;'>
    Built with ❤️ using Streamlit & Ollama
    </p>
    """,
    unsafe_allow_html=True
)
