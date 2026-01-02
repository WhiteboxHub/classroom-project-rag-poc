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

    # Assistant message
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Get pipeline from state
        pipeline = st.session_state.pipeline
        
        # Run query
        try:
            stream, sources = pipeline.run(prompt, stream=True)
            
            # Stream response
            for chunk in stream:
                if chunk.content:
                    full_response += chunk.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # Show sources
            if sources:
                with st.expander("View Request Sources"):
                    for i, doc in enumerate(sources):
                        page_num = doc['metadata'].get('page', 'N/A')
                        st.markdown(f"**Source {i+1} (Page {page_num})**")
                        st.text(doc['content'][:500] + "..." if len(doc['content']) > 500 else doc['content'])
            
            # Save response
            add_message("assistant", full_response)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

