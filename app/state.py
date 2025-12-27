import streamlit as st
from pipelines.query_pipeline import QueryPipeline
from db.models import ChatDatabase

def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "session_id" not in st.session_state:
        db = ChatDatabase()
        st.session_state.session_id = db.create_session()
        
    if "pipeline" not in st.session_state:
        st.session_state.pipeline = QueryPipeline()

def get_messages():
    return st.session_state.messages

def add_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})
    # Also save to DB
    db = ChatDatabase()
    db.add_message(st.session_state.session_id, role, content)
