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

## 🧪 Example Questions to Try
"What can I do at Jewel during a 6-hour layover?"
"Tell me about the attractions in Changi Terminal 3."
"Is there a cinema or garden in the airport?"
"Give a detailed plan for a family visit to Jewel."
"List food options in Terminal 1 with pictures."

## 🧠 How It Works
Web Scraping: The app fetches and cleans data from Changi and Jewel websites.
Chunking & Embedding: Text is split into 500-token chunks and embedded using SBERT.
Vector Search: FAISS returns the most relevant content for the user's query.
Gemini Generation: The chatbot uses Gemini 1.5 to generate responses from context.
TTS & Export: Users can listen to the reply or download it as a PDF.
