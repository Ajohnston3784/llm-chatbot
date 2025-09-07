import streamlit as st
from theme import get_theme

def load_css():
    theme = get_theme()
    is_dark = st.session_state.get("theme_mode", "dark") == "dark"
    
    transparent_base = "255, 255, 255" if is_dark else "0, 0, 0"
    shadow_opacity_heavy = "0.3" if is_dark else "0.1"
    shadow_opacity_light = "0.2" if is_dark else "0.05"
    css = f"""
    <style>
    /* === CSS VARIABLES === */
    :root {{
      /* Colors */
      --primary-color: {theme["PRIMARY_COLOR"]};
      --secondary-color: {theme["SECONDARY_COLOR"]};
      --background-color: {theme["BACKGROUND_COLOR"]};
      --chat-bg-color: {theme["CHAT_BG_COLOR"]};
      --user-msg-bg: {theme["USER_MSG_BG"]};
      --bot-msg-bg: {theme["BOT_MSG_BG"]};
      --text-color: {theme["TEXT_COLOR"]};
      --input-bg-color: {theme["INPUT_BG_COLOR"]};
      
      /* Transparent variations */
      --transparent-10: rgba({transparent_base}, 0.1);
      --transparent-20: rgba({transparent_base}, 0.2);
      --transparent-30: rgba({transparent_base}, 0.3);
      --transparent-50: rgba({transparent_base}, 0.5);
      --transparent-70: rgba({transparent_base}, 0.7);
      --transparent-80: rgba({transparent_base}, 0.8);
      --transparent-85: rgba({transparent_base}, 0.85);
      --transparent-90: rgba({transparent_base}, 0.9);
      
      /* Shadows */
      --box-shadow: 0 4px 12px rgba(0, 0, 0, {shadow_opacity_heavy});
      --light-shadow: 0 4px 12px rgba(0, 0, 0, {shadow_opacity_light});
      
      /* Border radius */
      --border-radius-sm: 4px;
      --border-radius-md: 6px;
      --border-radius-lg: 8px;
      --border-radius-xl: 10px;
    }}
    
    /* === GENERAL APP STYLING === */
    .stApp {{
        background-color: var(--background-color);
        color: var(--text-color);
        padding-top: 0 !important;
    }}
    
    /* Adjust main content padding */
    div.block-container {{
        padding-top: 0.5rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        padding-bottom: 1rem !important;
        max-width: 100% !important;
    }}
    
    /* Column alignment adjustments */
    div.row-widget.stHorizontalBlock > div:nth-child(2) {{
        margin-top: -25px; /* Raise the right column */
        padding-top: 0;
    }}
    
    /* Hide the default sidebar */
    [data-testid="stSidebar"] {{
        display: none !important;
    }}
    
    /* Hide the default Streamlit top menu bar */
    header[data-testid="stHeader"] {{
        display: none !important;
    }}
    
    /* Remove top padding that was meant for the header */
    section[data-testid="stAppViewContainer"] > div:first-child {{
        padding-top: 0rem !important;
    }}
    
    .main-title {{
        text-align: center; 
        font-size: 40px;
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 20px;
        margin-top: 5px;
    }}
    
    /* Common card styling */
    .card {{
        border-radius: var(--border-radius-lg);
        border: 1px solid var(--transparent-10);
        box-shadow: var(--box-shadow);
    }}
    
    /* === EXPANDER STYLING === */
    /* Group common expander styling */
    div[data-testid="stExpander"],
    div[data-testid="stExpander"] > details {{
      background: var(--chat-bg-color) !important;
      border-radius: var(--border-radius-lg) !important;
    }}
    
    div[data-testid="stExpander"] {{
      border: 1px solid var(--transparent-10) !important;
      margin-bottom: 0.4rem !important;
    }}
    
    /* Header row (the clickable summary) */
    div[data-testid="stExpander"] > details > summary {{
      background: var(--chat-bg-color) !important;
      color: var(--text-color) !important;
      border-radius: var(--border-radius-lg) !important;
      padding: 8px 10px !important;
    }}
    
    /* Body region when opened (covers current and older Streamlit DOMs) */
    div[data-testid="stExpander"] [data-testid="stExpanderContent"],
    div[data-testid="stExpander"] div[role="region"],
    div[data-testid="stExpander"] .streamlit-expanderContent {{
      background: var(--chat-bg-color) !important;
      color: var(--text-color) !important;
      border-radius: 0 0 var(--border-radius-lg) var(--border-radius-lg) !important;
      padding: 12px !important;
    }}
    
    /* Optional: keep nested white panels from showing up as white cards */
    div[data-testid="stExpander"] div[role="region"] > div {{
      background: transparent !important;
    }}
    
    .streamlit-expanderContent {{
        background-color: var(--chat-bg-color) !important;
        color: var(--text-color) !important;
    }}
                        
    /* === CHAT STYLING === */
    .chat-container {{
        height: 550px;
        overflow-y: auto;
        padding: 20px;
        border-radius: var(--border-radius-xl);
        background-color: var(--chat-bg-color);
        margin-bottom: 5px; /* Reduced margin to remove gap */
        border: 1px solid var(--transparent-10);
        box-shadow: var(--box-shadow);
    }}
    
    .chat-message {{
        padding: 1.5rem; 
        border-radius: 0.8rem; 
        margin-bottom: 1rem; 
        display: flex;
        flex-direction: column;
    }}
    
    .chat-message.user {{
        background-color: var(--user-msg-bg);
        border-top-right-radius: 0.2rem;
    }}
    
    .chat-message.bot {{
        background-color: var(--bot-msg-bg);
        border-top-left-radius: 0.2rem;
    }}
    
    .chat-message .message-content {{
        color: var(--text-color);
        font-size: 16px;
        margin-top: 0;
    }}
    
    .chat-message .message-metadata {{
        color: var(--transparent-70);
        font-size: 12px;
        margin-top: 8px;
        text-align: right;
    }}
    
    .chat-message .sources {{
        margin-top: 12px;
        font-size: 13px;
        color: var(--transparent-80);
    }}
    
    .chat-message .source-badge {{
        background-color: var(--transparent-20);
        padding: 2px 8px;
        border-radius: var(--border-radius-lg);
        margin-right: 4px;
        white-space: nowrap;
    }}
    
    /* === DOCUMENT LIST STYLING === */
    .document-list {{
        list-style-type: none;
        padding: 0;
        margin: 0;
    }}
    
    .document-list li {{
        background-color: var(--transparent-10);
        padding: 8px 12px;
        border-radius: var(--border-radius-sm);
        margin-bottom: 6px;
        color: var(--text-color);
    }}
    
    .query-container {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    /* === BUTTON STYLING === */
    /* Common button styles */
    .button-base {{
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: var(--border-radius-md);
        font-weight: bold;
        transition: all 0.3s;
    }}
    
    .button-base:hover {{
        background-color: var(--secondary-color);
        transform: translateY(-2px);
        box-shadow: var(--light-shadow);
    }}
    
    /* Standard buttons */
    .stButton > button {{
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: var(--border-radius-md);
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s;
    }}
    
    .stButton > button:hover {{
        background-color: var(--secondary-color);
        transform: translateY(-2px);
        box-shadow: var(--light-shadow);
    }}
    
    /* === TEXT INPUT STYLING === */
    /* Style for the input field label - make sure it's visible in both themes */
    .stTextInput label, .stTextArea label, .stSelectbox label, .stFileUploader label,
    div[data-baseweb="select"] > div > label, div[data-baseweb="base-input"] > label {{
        color: var(--text-color) !important;
    }}
    
    /* Remove extra space around the text input */
    .stTextInput {{
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }}
    
    .stTextInput > div > div > input {{
        background-color: var(--input-bg-color);
        border: 1px solid var(--transparent-20);
        color: var(--text-color) !important;
        border-radius: var(--border-radius-md);
        padding: 12px;
    }}
    
    /* Ensure placeholder text is visible in both themes */
    .stTextInput > div > div > input::placeholder {{
        color: var(--transparent-70) !important;
        opacity: 1 !important;
    }}
    
    .sidebar-title {{
        font-size: 22px;
        margin-bottom: 10px;
        color: var(--text-color);
    }}
    
    /* === FILE UPLOADER STYLING === */
    /* Base uploader styles */
    div[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"],
    .stFileUploader > div > div {{
      background-color: var(--input-bg-color) !important;
      border: 2px dashed var(--transparent-30) !important;
      border-radius: var(--border-radius-lg) !important;
    }}
    
    div[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"]:hover,
    .stFileUploader > div > div:hover {{
      border-color: var(--transparent-50) !important;
    }}
    
    /* Uploader text styling */
    div[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] *,
    .stFileUploader > div > div * {{
      color: var(--transparent-85) !important;
    }}
    
    div[data-testid="stFileUploader"] label,
    div[data-testid="stFileUploader"] p,
    div[data-testid="stFileUploader"] small {{
      color: var(--transparent-90) !important;
    }}
    
    /* Specific text elements */
    div[data-testid="stFileUploader"] label {{
        font-weight: 500;
    }}
    
    div[data-testid="stFileUploader"] small {{
        color: var(--transparent-70) !important;
    }}
    
    /* Button styling in file uploader */
    div[data-testid="stFileUploader"] button,
    div[data-testid="stFileUploader"] label[role="button"],
    div[data-testid="stFileUploader"] [data-testid="baseButton-primary"],
    div[data-testid="stFileUploader"] [data-testid="baseButton-secondary"],
    div[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] button,
    div[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] label[role="button"] {{
      /* Common button properties */
      padding: 6px 10px !important;
      font-size: 0.85rem !important;
      line-height: 1.1 !important;
      min-height: 0 !important;
      border-radius: var(--border-radius-md) !important;
      background-color: var(--primary-color) !important;
      color: white !important;
      border: none !important;
      box-shadow: var(--light-shadow) !important;
      transition: all 0.3s;
    }}
    
    div[data-testid="stFileUploader"] button:hover,
    div[data-testid="stFileUploader"] label[role="button"]:hover,
    div[data-testid="stFileUploader"] [data-testid="baseButton-primary"]:hover,
    div[data-testid="stFileUploader"] [data-testid="baseButton-secondary"]:hover,
    div[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] button:hover,
    div[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] label[role="button"]:hover {{
      background-color: var(--secondary-color) !important;
      transform: translateY(-1px);
    }}
    
    /* Special styling for the X button */
    div[data-testid="stFileUploader"] button:has(svg) {{
      width: 28px !important;
      height: 28px !important;
      min-width: 28px !important;
      min-height: 28px !important;
      padding: 4px !important;
      border-radius: var(--border-radius-lg) !important;
    }}
    
    div[data-testid="stFileUploader"] button svg {{
      width: 14px !important;
      height: 14px !important;
    }}
    
    /* Filename styling */
    div[data-testid="stFileUploader"] [data-testid="stFileUploaderFileName"] {{
      color: var(--text-color) !important;
      font-weight: 600 !important;
      background: var(--transparent-10) !important;
      padding: 6px 10px !important;
      border-radius: var(--border-radius-md) !important;
    }}
    
    div[data-testid="stFileUploader"] [data-testid="stFileSize"] {{
      color: var(--transparent-70) !important;
    }}
    
    .uploadedFileName {{
        color: var(--text-color) !important;
        background-color: var(--transparent-20) !important;
        padding: 5px 10px !important;
        border-radius: var(--border-radius-sm) !important;
        margin-top: 8px !important;
    }}
    
    /* === FOOTER STYLING === */
    .footer-text, .footer-text * {{
        color: var(--transparent-50) !important;
        text-decoration: none !important;
        pointer-events: none !important;
        user-select: none !important;
    }}
    
    /* === THEME TOGGLE BUTTON === */
    .theme-toggle-btn {{
        position: fixed;
        top: 10px;
        right: 10px;
        font-size: 24px;
        background: transparent;
        border: none;
        cursor: pointer;
        z-index: 9999;
    }}
    
    /* Style for the theme button at top left */
    button[key="theme-toggle-btn"] {{
        margin-top: 10px !important;
        margin-bottom: 15px !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# JavaScript for chat auto-scrolling
SCROLL_JS = """
<style>
#chat-container { position: relative; scroll-behavior: smooth; }
#chat-new-msg {
  position: absolute; right: 12px; bottom: 12px;
  padding: 6px 10px; font-size: 12px; font-weight: 700;
  border-radius: 999px; border: none;
  background: var(--primary-color); color: #fff; box-shadow: var(--light-shadow);
  display: none; cursor: pointer; z-index: 2;
}
</style>
<script>
(function () {
  function init() {
    const el = document.getElementById('chat-container');
    if (!el) { setTimeout(init, 50); return; }
    if (el.dataset.scrollbound === '1') return;
    el.dataset.scrollbound = '1';

    let userPinnedUp = sessionStorage.getItem('chatPinnedUp') === '1';
    const tol = 24;
    const isAtBottom = () => (el.scrollHeight - el.scrollTop - el.clientHeight) <= tol;

    const setPinned = (v) => {
      userPinnedUp = v;
      sessionStorage.setItem('chatPinnedUp', v ? '1' : '0');
      newBtn.style.display = v ? 'block' : 'none';
    };

    let newBtn = document.getElementById('chat-new-msg');
    if (!newBtn) {
      newBtn = document.createElement('button');
      newBtn.id = 'chat-new-msg';
      newBtn.textContent = 'Jump to latest';
      el.appendChild(newBtn);
    }
    newBtn.addEventListener('click', () => { setPinned(false); el.scrollTop = el.scrollHeight; });

    el.addEventListener('scroll', () => setPinned(!isAtBottom()));

    const mo = new MutationObserver(() => {
      if (!userPinnedUp) { el.scrollTop = el.scrollHeight; }
      else { newBtn.style.display = 'block'; }
    });
    mo.observe(el, { childList: true, subtree: true });

    if (!userPinnedUp) el.scrollTop = el.scrollHeight;
  }
  init();
})();
</script>
"""
