# changi_ultimate_infobot.py
# 🚀 Changi InfoBot: Ultra Advanced Streamlit + LangChain + Gemini + FAISS + TTS + Images + PDF Export

import os
import faiss
import pickle
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import streamlit as st
from sentence_transformers import SentenceTransformer
from fpdf import FPDF
from gtts import gTTS
from PIL import Image
import io
import google.generativeai as genai

# === 🔐 Load Gemini API Key ===
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("❌ Please set GEMINI_API_KEY in your .env file.")
    st.stop()

# === 🔮 Configure Gemini ===
genai.configure(api_key=GEMINI_API_KEY)
gemini = genai.GenerativeModel("gemini-1.5-flash")

# === 🧠 SBERT Model ===
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# === 🌐 URLs for Scraping ===
URLS = [
    "https://www.changiairport.com/en/airport-guide.html",
    "https://www.jewelchangiairport.com/en/attractions.html"
]

# === 📥 Scrape + Clean + Collect Images ===
@st.cache_data(show_spinner="🔍 Scraping content...")
def scrape_site(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    images = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs and img['src'].startswith("http")]
    return text, images

# === ✂️ Chunk Text ===
def chunk_text(text, size=500):
    return [text[i:i+size] for i in range(0, len(text), size)]

# === 📦 FAISS DB ===
@st.cache_resource(show_spinner="📦 Building vector DB...")
def get_vector_db():
    db_file = "changi_vector.pkl"
    if os.path.exists(db_file):
        with open(db_file, "rb") as f:
            return pickle.load(f)
    all_text, all_imgs = "", []
    for url in URLS:
        t, imgs = scrape_site(url)
        all_text += t + "\n"
        all_imgs.extend(imgs)
    chunks = chunk_text(all_text)
    vectors = embedder.encode(chunks)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    with open(db_file, "wb") as f:
        pickle.dump((index, vectors, chunks, all_imgs), f)
    return index, vectors, chunks, all_imgs

# === 🔍 Retrieve Context ===
def retrieve_context(query, index, chunks, k=3):
    query_vec = embedder.encode([query])
    _, I = index.search(query_vec, k)
    return "\n".join([chunks[i] for i in I[0]])

# === 💬 Ask Gemini ===
def ask_gemini(question, context):
    prompt = f"""
Answer the question using ONLY the below Changi Airport & Jewel content:

Context:
{context}

Question:
{question}

Please explain in detail with examples.
"""
    try:
        response = gemini.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ AI Error: {e}"

# === 📄 PDF Download ===
def export_pdf(answer):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, answer)
    path = "answer.pdf"
    pdf.output(path)
    return path

# === 🔊 TTS ===
def speak_text(answer):
    tts = gTTS(text=answer)
    tts.save("answer.mp3")
    return "answer.mp3"

# === 🌟 UI Layout ===
st.set_page_config("Changi InfoBot Pro", layout="wide", page_icon="🛬")
with st.sidebar:
    st.title("🛬 About This App")
    st.info("AI chatbot trained on Changi Airport & Jewel website")
    st.markdown("- ✅ Detailed Explanations\n- ✅ Image Support\n- ✅ Export to PDF & Listen")
    st.success("Built with Gemini + FAISS + SBERT + Streamlit")

st.markdown("""
    <h1 style='color:#005a9c;'>🌐 Changi Airport AI InfoBot Pro</h1>
    <p>Ask anything about Changi Airport or Jewel and get advanced answers with images, PDF export, and voice!</p>
""", unsafe_allow_html=True)

query = st.text_input("✍️ Your question", placeholder="What to do at Jewel during layovers?")
col1, col2, col3 = st.columns(3)

if col1.button("🔍 Get Answer"):
    index, vectors, chunks, images = get_vector_db()
    context = retrieve_context(query, index, chunks)
    with st.spinner("💬 AI is crafting your answer..."):
        answer = ask_gemini(query, context)
    st.success("✅ Here's the response:")
    st.write(answer)

    with col2:
        if st.button("📄 Download as PDF"):
            path = export_pdf(answer)
            with open(path, "rb") as f:
                st.download_button("📥 Save PDF", f, file_name="changi_answer.pdf")

    with col3:
        if st.button("🔊 Listen to Answer"):
            audio = speak_text(answer)
            st.audio(audio)

    # Optional Images
    st.markdown("---")
    st.markdown("### 📸 Related Visuals:")
    for img_url in images[:3]:
        try:
            img_data = requests.get(img_url).content
            st.image(Image.open(io.BytesIO(img_data)), caption=img_url.split("/")[-1])
        except:
            pass
