import streamlit as st
import requests

from config import API_BASE

def display_document_upload():
    st.markdown('<h2 class="sidebar-title" style="margin-top: -5px; margin-bottom: 10px;">📄 Document Management</h2>', unsafe_allow_html=True)
    
    if "file_uploaded" not in st.session_state:
        st.session_state.file_uploaded = {}
    
    with st.expander("📤 Upload New Document", expanded=True):
        uploaded_file = st.file_uploader("Choose a file", key="file_uploader")
        upload_button = st.button("Upload Document", use_container_width=True)
        
        if upload_button and uploaded_file:
            # Check if we've already uploaded this file (based on name and size)
            file_key = f"{uploaded_file.name}_{uploaded_file.size}"
            
            if file_key not in st.session_state.file_uploaded:
                with st.status("Uploading document...", expanded=True) as status:
                    st.write(f"Processing {uploaded_file.name}...")
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    
                    try:
                        # Upload to the backend
                        upload_url = f"{API_BASE}/upload/"
                        response = requests.post(upload_url, files=files, timeout=20)
                        
                        if response.status_code == 200:
                            status.update(label="Upload complete!", state="complete", expanded=False)
                            st.success(f"✅ Successfully uploaded: {uploaded_file.name}")
                            # Mark this file as uploaded so we don't upload it again
                            st.session_state.file_uploaded[file_key] = True
                        else:
                            status.update(label="Upload failed!", state="error", expanded=True)
                            st.error(f"❌ Failed: {response.text}")
                            is_dark = st.session_state.get("theme_mode", "dark") == "dark"
                            text_color = "rgba(255,255,255,0.7)" if is_dark else "rgba(0,0,0,0.7)"
                            st.markdown(f"<div style='color: {text_color};'>Response status: {response.status_code}</div>", unsafe_allow_html=True)
                    
                    except Exception as e:
                        status.update(label="Upload error!", state="error", expanded=True)
                        st.error(f"❌ Error: {str(e)}")
            else:
                is_dark = st.session_state.get("theme_mode", "dark") == "dark"
                text_color = "rgba(255,255,255,0.7)" if is_dark else "rgba(0,0,0,0.7)"
                bg_color = "rgba(255,255,255,0.1)" if is_dark else "rgba(0,0,0,0.05)"
                st.markdown(f"<div style='color: {text_color}; padding: 5px 10px; background-color: {bg_color}; border-radius: 4px;'>File {uploaded_file.name} already uploaded</div>", unsafe_allow_html=True)

def display_document_list():
    """Display the list of uploaded documents in the sidebar"""

    is_dark = st.session_state.get("theme_mode", "dark") == "dark"
    text_color = "rgba(255,255,255,0.7)" if is_dark else "rgba(0,0,0,0.7)"
    
    with st.expander("📝 Uploaded Documents", expanded=True):
        # List already uploaded documents
        if st.session_state.file_uploaded:
            st.markdown("<ul class='document-list'>", unsafe_allow_html=True)
            for file_key in st.session_state.file_uploaded:
                filename = file_key.split('_')[0]
                st.markdown(f"<li><i class='fas fa-file-alt'></i> {filename}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color: {text_color}; padding: 10px; text-align: center;'>No documents uploaded yet</div>", unsafe_allow_html=True)

def display_about_section():
    """Display the about section in the sidebar"""

    is_dark = st.session_state.get("theme_mode", "dark") == "dark"
    text_color = "white" if is_dark else "#333333"
    
    with st.expander("ℹ️ About this AI Assistant"):
        st.markdown(f"""
        <div style="color: {text_color};">
        This AI assistant is powered by:
        <ul>
            <li>LangChain for document processing</li>
            <li>Chroma vector database for semantic search</li>
            <li>OpenAI models for embeddings and generation</li>
            <li>FastAPI backend and Streamlit frontend</li>
        </ul>
        <p>Created for portfolio demonstration.</p>
        </div>
        """, unsafe_allow_html=True)