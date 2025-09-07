import streamlit as st

DARK_MODE = {
    "PRIMARY_COLOR": "#4a00e0",
    "SECONDARY_COLOR": "#8e2de2",
    "BACKGROUND_COLOR": "#1e2130",
    "CHAT_BG_COLOR": "#272e3f",
    "USER_MSG_BG": "#2b313e",
    "BOT_MSG_BG": "#475063",
    "INPUT_BG_COLOR": "#2b313e",
    "TEXT_COLOR": "#ffffff"
}

LIGHT_MODE = {
    "PRIMARY_COLOR": "#6200ee",
    "SECONDARY_COLOR": "#3700b3", 
    "BACKGROUND_COLOR": "#f7f7f9",
    "CHAT_BG_COLOR": "#ffffff",
    "USER_MSG_BG": "#e8f0fe",
    "BOT_MSG_BG": "#f1f3f4",
    "INPUT_BG_COLOR": "#ffffff",
    "TEXT_COLOR": "#333333"
}

def get_theme():
    """Get the current theme colors based on session state"""
    
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "dark"
    
    return DARK_MODE if st.session_state.theme_mode == "dark" else LIGHT_MODE

def toggle_theme():
    """Toggle between light and dark mode"""

    previous_theme = st.session_state.theme_mode
    
    if st.session_state.theme_mode == "dark":
        st.session_state.theme_mode = "light"
    else:
        st.session_state.theme_mode = "dark"
    
    new_theme = st.session_state.theme_mode
    st.sidebar.success(f"Theme changed: {previous_theme} → {new_theme}")
    
    st.session_state.theme_was_toggled = True
