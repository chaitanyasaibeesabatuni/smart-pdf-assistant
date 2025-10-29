import streamlit as st
import time
import os
from streamlit_lottie import st_lottie
import json
import requests
import utils  # your custom module

# --------------------------- Page configuration ---------------------------
st.set_page_config(
    page_title="Smart PDF Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------- Custom CSS ---------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }
    
    /* Increase sidebar width */
    section[data-testid="stSidebar"] {
        width: 350px !important;
        min-width: 350px !important;
    }

    /* --- Main Header --- */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeIn 1.5s ease-in;
    }

    /* --- Cards --- */
    .info-card {
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(12px);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        animation: slideIn 0.6s ease-out;
    }

    .success-message, .warning-message {
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        animation: fadeIn 0.8s ease-in;
    }
    .success-message {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        box-shadow: 0 8px 25px rgba(72, 187, 120, 0.3);
    }
    .warning-message {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        box-shadow: 0 8px 25px rgba(237, 137, 54, 0.3);
    }

    .ai-response-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
        animation: fadeIn 1s ease;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideIn {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    @keyframes floatUp {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
</style>
""", unsafe_allow_html=True)

# --------------------------- Lottie Loader ---------------------------
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Animations
welcome_animation = "https://assets1.lottiefiles.com/packages/lf20_gn0tojcq.json"
upload_animation = "https://assets1.lottiefiles.com/packages/lf20_5tkzkblw.json"
question_animation = "https://assets1.lottiefiles.com/packages/lf20_7sk0mcix.json"

# --------------------------- Sidebar ---------------------------
with st.sidebar:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 1rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 1.5rem;
        color: white;
        font-size: 1.5rem;
        font-weight: 800;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: -30px;
            right: -15px;
            width: 60px;
            height: 60px;
            background: rgba(255,255,255,0.15);
            border-radius: 50%;
        "></div>
        <div style="
            position: absolute;
            bottom: -20px;
            left: -15px;
            width: 50px;
            height: 50px;
            background: rgba(255,255,255,0.15);
            border-radius: 50%;
        "></div>
        <div style="position: relative; z-index: 2;">
            📚 Smart PDF Assistant
            <div style="font-size: 0.7rem; opacity: 0.9; margin-top: 5px;">✨ Intelligent Document Analysis ✨</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Role Selection Card
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.95);
        padding: 1.2rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(10px);
    ">
        <div style="
            text-align: center;
            margin-bottom: 0.8rem;
        ">
            <span style='
                font-weight: 700;
                color: #667eea;
                font-size: 1.1rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            '>👤 Select Your Role 🌟</span>
        </div>
    """, unsafe_allow_html=True)

    page = st.selectbox('', ['Click Here', 'Admin', 'User'], index=0,
                        help="Choose 'Admin' to upload PDFs or 'User' to ask questions.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Animation Section - Simplified without extra container
    if page == "Admin":
        anim = load_lottie_url(upload_animation)
        if anim: 
            st_lottie(anim, height=140, key="admin_lottie")
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
            padding: 0.5rem 0.8rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-block;
            margin-top: 0.5rem;
            text-align: center;
            width: 100%;
        ">
            ⚙️ Admin Mode
        </div>
        """, unsafe_allow_html=True)
    elif page == "User":
        anim = load_lottie_url(question_animation)
        if anim: 
            st_lottie(anim, height=140, key="user_lottie")
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
            color: white;
            padding: 0.5rem 0.8rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-block;
            margin-top: 0.5rem;
            text-align: center;
            width: 100%;
        ">
            💬 User Mode
        </div>
        """, unsafe_allow_html=True)
    else:
        anim = load_lottie_url(welcome_animation)
        if anim: 
            st_lottie(anim, height=140, key="welcome_lottie")

    # Quick Stats/Info Section
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem;
        border-radius: 15px;
        margin-top: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
    ">
        <div style="font-size: 0.85rem; color: #666; line-height: 1.4;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="margin-right: 0.5rem;">🔒</span>
                <span>Secure & Private</span>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="margin-right: 0.5rem;">⚡</span>
                <span>Fast Processing</span>
            </div>
            <div style="display: flex; align-items: center;">
                <span style="margin-right: 0.5rem;">🤖</span>
                <span>AI Powered</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
# --------------------------- Home Page ---------------------------
if page not in ['Admin', 'User']:
    st.markdown('<div class="main-header">Welcome to Smart PDF Assistant 🚀</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>🤖 What is Smart PDF Assistant?</h3>
            <p>This intelligent system lets you upload PDF documents and interact with them conversationally.
            It uses advanced AI embeddings and retrieval-augmented generation (RAG) techniques to answer your questions contextually.</p>
        </div>
        <div class="info-card">
            <h3>⚙️ How It Works</h3>
            <ol style="line-height:1.8;">
                <li><b>Admin uploads</b> a PDF, which is split into chunks and converted into vector embeddings.</li>
                <li><b>Database stores</b> these chunks for retrieval.</li>
                <li><b>User asks</b> a question — the AI fetches relevant chunks and generates a context-rich answer.</li>
            </ol>
        </div>
        <div class="info-card" style="animation: floatUp 3s infinite;">
            <h3>💡 Example Use Cases</h3>
            <ul style="line-height:1.8;">
                <li>Summarizing research papers</li>
                <li>Understanding legal or business documents</li>
                <li>Extracting key facts from reports</li>
                <li>Answering knowledge base queries</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        anim = load_lottie_url(welcome_animation)
        if anim: st_lottie(anim, height=420)

# --------------------------- Admin Page ---------------------------
elif page == "Admin":
    st.markdown('<div class="main-header">Admin Dashboard ⚙️</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="info-card"><h3>📤 Upload & Process PDFs</h3><p>Upload a PDF to convert it into intelligent embeddings stored in the local database.</p></div>', unsafe_allow_html=True)
        uploader_file = st.file_uploader('📎 Upload your PDF file', type='pdf')
        if uploader_file:
            with st.spinner("🔄 Processing your PDF..."):
                os.makedirs("pdfs", exist_ok=True)
                pdf_path = os.path.join("pdfs", uploader_file.name)
                with open(pdf_path, "wb") as f:
                    f.write(uploader_file.getbuffer())

                text = utils.pdf_reader(pdf_path)
                text_chunks = utils.text_chunking(text)
                utils.save_into_db(text_chunks)

                st.markdown(f"""
                <div class="success-message">
                    <h4>✅ Success!</h4>
                    <p><b>{uploader_file.name}</b> processed and stored successfully.</p>
                </div>
                """, unsafe_allow_html=True)
    with col2:
        anim = load_lottie_url(upload_animation)
        if anim: st_lottie(anim, height=300)

# --------------------------- User Page ---------------------------
elif page == "User":
    st.markdown('<div class="main-header">Ask Your PDF Assistant 💬</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.8, 1.2])
    with col1:
        st.markdown('<div class="info-card"><h3>🧠 Ask a Question</h3><p>Query your PDF using natural language and receive precise AI-generated responses.</p></div>', unsafe_allow_html=True)
        query = st.text_input("💭 Ask a question:", placeholder="e.g., Summarize section 4 or list the recommendations")
        if st.button("🚀 Get Answer", use_container_width=True) and query:
            with st.spinner("🤖 Generating answer..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.008)
                    progress_bar.progress(i + 1)
                try:
                    db = utils.load_db()
                    answer = utils.answer_generator(query, db)
                    st.markdown(f"""
                    <div class="ai-response-card">
                        <h4>✨ AI Response</h4>
                        <p>{answer}</p>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"""
                    <div class="warning-message">
                        <h4>⚠️ Error!</h4>
                        <p>{str(e)}</p>
                        <p>Ensure Admin has uploaded and processed PDFs first.</p>
                    </div>
                    """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #8EC5FC 0%, #E0C3FC 100%);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 25px rgba(142,197,252,0.4);
            animation: floatUp 3s ease-in-out infinite alternate;
        ">
            <h3 style="text-align:center;">💡 Example Prompts</h3>
            <ul style="font-size: 1.05rem; line-height: 1.9;">
                <li>📘 Summarize the introduction</li>
                <li>📄 List key terms explained</li>
                <li>📊 Compare two models discussed</li>
                <li>💬 What are the recommendations?</li>
                <li>🧾 Explain main results briefly</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)