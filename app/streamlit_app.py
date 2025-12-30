import streamlit as st
from app.state import init_state, add_message, get_messages

st.set_page_config(page_title="RAG POC", layout="wide")

# Initialize State
init_state()

st.title("📚 Provider Manual RAG Chat")

# Sidebar for controls
with st.sidebar:
    st.header("Settings")
    if st.button("Reset Conversation"):
        st.session_state.messages = []
        st.rerun()

# Display Chat History
for msg in get_messages():
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask a question about the provider manual..."):
    # User message
    add_message("user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        pipeline = st.session_state.pipeline

        try:
            answer, sources = pipeline.run(prompt, stream=False)

            message_placeholder.markdown(answer)

            # Show sources
            if sources:
                with st.expander("View Request Sources"):
                    for i, doc in enumerate(sources):
                        st.markdown(
                            f"**Source {i+1} (Page {doc['metadata'].get('page')})**"
                        )
                        st.text(doc["content"])

            add_message("assistant", answer)

        except Exception as e:
            st.error(f"An error occurred: {e}")
