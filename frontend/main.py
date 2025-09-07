import streamlit as st

from config import APP_TITLE, APP_ICON, APP_HEADER
from styles import load_css
from components.chat import display_chat_container, display_chat_input, handle_chat_query
from components.sidebar import display_document_upload, display_document_list, display_about_section
from components.theme_toggle import display_theme_toggle

def main():
    st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "dark"
    
    if "theme_was_toggled" in st.session_state and st.session_state.theme_was_toggled:
        st.session_state.theme_was_toggled = False
        st.rerun()

    load_css()
    
    st.markdown("""
    <style>
    .block-container {
        padding-bottom: 0 !important;
    }
    
    .stMarkdown:has(p:contains("Ask a question about your documents:")) {
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }
    
    .stMarkdown + .element-container {
        margin-top: -15px !important;
    }
    
    .element-container {
        margin-bottom: 0 !important;
    }
    
    .stTextInput {
        margin-top: -10px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    display_theme_toggle()

    st.markdown(f'<h1 class="main-title">{APP_HEADER}</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1], gap="large")

    with col1:
        _, chat_area = display_chat_container()
        
        st.markdown("""
        <div style="margin:0; padding:0; line-height:1; margin-bottom:-15px;">Ask a question about your documents:</div>
        <style>
        .stTextInput {
            margin-top: -5px !important;
            padding-top: 0 !important;
        }
        .element-container + .element-container {
            margin-top: -15px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        ask_button, query = display_chat_input()
        
        if "submitted_query" not in st.session_state:
            st.session_state.submitted_query = ""

        current_query = st.session_state.submitted_query if st.session_state.submitted_query else query
        if (ask_button or st.session_state.submitted_query) and current_query:
            handle_chat_query(chat_area, current_query)

    with col2:
        display_document_upload()
        display_document_list()
        display_about_section()

if __name__ == "__main__":
    main()
