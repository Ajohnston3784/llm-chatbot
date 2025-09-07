import textwrap
from datetime import datetime
import streamlit as st

def build_chat_html(history):
    """
    Build HTML string for the chat messages from the history
    """
    import streamlit as st
    
    # Get appropriate text color based on theme
    is_dark = st.session_state.get("theme_mode", "dark") == "dark"
    text_color = "#ffffff" if is_dark else "#333333"
    meta_color = "rgba(255,255,255,0.7)" if is_dark else "rgba(0,0,0,0.6)"
    
    parts = []
    for q, a, srcs in history:
        t = datetime.now().strftime("%I:%M %p")
        src_html = ""
        if srcs:
            badges = " ".join([f'<span class="source-badge">{s}</span>' for s in srcs])
            src_html = f'<div class="sources">Sources: {badges}</div>'

        user_html = textwrap.dedent(f"""
        <div class="chat-message user">
          <div class="message-content" style="color: {text_color};">{q}</div>
          <div class="message-metadata" style="color: {meta_color};">You • {t}</div>
        </div>
        """).strip()

        bot_html = textwrap.dedent(f"""
        <div class="chat-message bot">
          <div class="message-content" style="color: {text_color};">{a}</div>
          {src_html}
          <div class="message-metadata" style="color: {meta_color};">AI Assistant • {t}</div>
        </div>
        """).strip()

        parts.append(user_html)
        parts.append(bot_html)

    return "".join(parts)


def get_welcome_message():
    
    is_dark = st.session_state.get("theme_mode", "dark") == "dark"
    text_color = "rgba(255,255,255,0.5)" if is_dark else "rgba(0,0,0,0.6)"
    
    return textwrap.dedent(f"""
    <div style="text-align:center; color: {text_color}; margin-top: 200px;">
    <p>👋 Hello! I'm your AI document assistant.</p>
    <p>Upload documents and ask questions about them.</p>
    </div>
    """).strip()
