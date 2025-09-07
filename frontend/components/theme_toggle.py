import streamlit as st
from theme import toggle_theme

def display_theme_toggle():
    """Display a toggle button for switching between light and dark mode"""
    
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "dark"
    
    current_theme = st.session_state.theme_mode
    light_icon = "☀️" 
    dark_icon = "🌙"
    tooltip = "Switch to Light Mode" if current_theme == "dark" else "Switch to Dark Mode"
    current_icon = dark_icon if current_theme == "dark" else light_icon
    
    top_row = st.container()
    with top_row:
        left_col, right_col = st.columns([2, 10])
        
        with left_col:
            st.button(
                f"{current_icon} {current_theme.capitalize()}",
                key="theme-toggle-btn",
                on_click=toggle_theme,
                help=tooltip,
                type="primary",
            )
