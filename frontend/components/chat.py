import streamlit as st
import requests
import textwrap
from datetime import datetime

from config import API_BASE
from styles import SCROLL_JS
from components.utils import build_chat_html, get_welcome_message

def render_chat(html: str, chat_area):
    chat_area.markdown(f'<div class="chat-container" id="chat-container">{html}</div>', unsafe_allow_html=True)
    st.markdown(SCROLL_JS, unsafe_allow_html=True)

def display_chat_container():
    """Display the chat container with messages from history"""

    if "history" not in st.session_state:
        st.session_state["history"] = []
    
    chat_container = st.container()
    with chat_container:
        chat_area = st.empty()
        
        if not st.session_state["history"]:
            chat_content = get_welcome_message()
        else:
            chat_content = build_chat_html(st.session_state["history"])

        render_chat(chat_content, chat_area)
        
    return chat_container, chat_area

def display_chat_input():
    """Display the chat input area and handle user queries"""
 
    if "query" not in st.session_state:
        st.session_state.query = ""
    
    def submit_query():
        if st.session_state.query.strip():
            st.session_state.submitted_query = st.session_state.query
            st.session_state.query = ""
    
    is_dark = st.session_state.get("theme_mode", "dark") == "dark"
    text_color = "#ffffff" if is_dark else "#333333"
    
    st.markdown(f"""
    <style>
    .chat-input-label {{
        color: {text_color} !important;
        font-weight: 500;
        margin: 0 !important;
        padding: 0 !important;
    }}
    .element-container:has(.chat-input-label) {{
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    input_style = f"""
    <style>
    .stTextInput input {{
        color: {text_color} !important;
    }}
    .stTextInput input::placeholder {{
        color: rgba({255 if is_dark else 0}, {255 if is_dark else 0}, {255 if is_dark else 0}, 0.6) !important;
    }}
    .stTextInput {{
        margin-top: -10px !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }}
    .element-container:has(.stTextInput) {{
        margin-top: -15px !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }}
    .stTextInput > div {{
        margin-top: 0 !important;
        padding-top: 0 !important;
    }}
    </style>
    """
    st.markdown(input_style, unsafe_allow_html=True)
    
    query = st.text_input(
        " ",
        key="query", 
        placeholder="What would you like to know?",
        on_change=submit_query
    )
    
    col_btn_1, col_btn_2 = st.columns([4, 1])
    with col_btn_2:
        ask_button = st.button("Ask", use_container_width=True, on_click=submit_query)
    
    return ask_button, query

def handle_chat_query(chat_area, current_query):
    """Handle the chat query submission and update the chat area"""
    
    ts = datetime.now().strftime("%I:%M %p")
    thinking_html = textwrap.dedent(f"""
    <div class="chat-message user">
    <div class="message-content">{current_query}</div>
    <div class="message-metadata">You • {ts}</div>
    </div>
    <div class="chat-message bot">
    <div class="message-content"><em>Thinking…</em></div>
    <div class="message-metadata">AI Assistant • {ts}</div>
    </div>
    """).strip()

    chat_area.markdown(
        f'<div class="chat-container" id="chat-container">{(build_chat_html(st.session_state["history"]) + thinking_html) if st.session_state["history"] else thinking_html}</div>',
        unsafe_allow_html=True
    )

    try:
        resp = requests.post(f"{API_BASE}/chat/", json={"query": current_query}, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            answer, sources = data.get("answer", ""), data.get("sources", [])
        else:
            answer = f"**Error**: {resp.text}"
            sources = []
    except Exception as e:
        answer = f"**Error**: {e}"
        sources = []

    st.session_state.history.append((current_query, answer, sources))
    chat_area.markdown(
        f'<div class="chat-container" id="chat-container">{build_chat_html(st.session_state["history"])}</div>',
        unsafe_allow_html=True
    )
    st.session_state.submitted_query = ""

    st.markdown("""
        <script>
            var div = document.getElementById('chat-container');
            if (div) div.scrollTop = div.scrollHeight;
        </script>
    """, unsafe_allow_html=True)
