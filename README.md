# 🛬 Changi Airport AI InfoBot Pro

An advanced, multimodal chatbot that provides real-time answers to questions about **Changi Airport** and **Jewel Changi Airport**, powered by **Google Gemini 1.5 Flash**, **FAISS**, and **SBERT embeddings**. Built with **Streamlit**, it supports PDF export, voice answers, and image rendering — designed for high performance, extensibility, and rich UX.

---

## 🚀 Features

- ✅ **Retrieval-Augmented Generation (RAG)** chatbot
- 🔮 **Gemini 1.5 Flash** for intelligent, contextual responses
- 🧠 **SBERT + FAISS** for semantic vector search
- 🎤 **Voice Output** using `gTTS`
- 📸 **Image extraction** from Changi & Jewel websites
- 📄 **PDF export** of answers
- 🧼 Real-time **web scraping & text cleaning**
- 💡 **Streamlit UI** — clean, professional, and responsive

---

## 🧠 Architecture Overview

```text
[User Input]
    ↓
[SBERT Embedding]
    ↓
[FAISS Vector DB Retrieval]
    ↓
[Context + Question]
    ↓
[Gemini 1.5 Flash Response]
    ↓
[Streamlit Display + TTS + PDF + Images]

