# 👁️ Vision Intelligence: Semantic Video Tracking & Attribute Extraction

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![YOLO](https://img.shields.io/badge/YOLOv11-00FFFF?style=for-the-badge&logo=YOLO&logoColor=black)
![Ollama](https://img.shields.io/badge/Ollama_Local_VLM-FFFFFF?style=for-the-badge&logo=Ollama&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

An end-to-end Computer Vision pipeline designed for **Automated Person Tracking and Semantic Attribute Extraction** from video footage. This system intelligently combines Real-time Object Detection, Multi-Object Tracking, and Vision Language Models (VLM) to catalog human subjects based on their physical attributes (gender, clothing color, outfit type).

## ✨ Key Features & Engineering Highlights

- **Smart Subject Isolation (Area Thresholding):** Integrates YOLOv11 with custom logic to filter out background crowds/dancers, focusing exclusively on the primary subject (e.g., detecting only the main artist in a fancam by thresholding bounding box area > 15%).
- **Time-Based Sampling for Dynamic Scenes:** Addresses the "OOTD (Outfit of The Day) Problem" by sampling tracked IDs every 3 seconds, ensuring the system captures wardrobe transitions seamlessly without overloading the database or GPU.
- **Zero-Hallucination VLM Pipeline:** Utilizes local LLM/VLM (`qwen2.5vl:3b` via Ollama) with strict prompt engineering and `temperature=0.0` to force deterministic JSON outputs, preventing AI hallucinations when identifying clothing patterns and colors.
- **Robust Multi-Object Tracking:** Uses ByteTrack algorithm to maintain consistent IDs across frames, even amidst occlusions or rapid movements.
- **Full-Stack Semantic Search Dashboard:** A modern React/Vite frontend featuring:
  - Natural Language Filtering (Search by Gender, Shirt Color, etc.)
  - Interactive Lightbox for verification.
  - Complete Storage Management (Clean Garbage Collection that deletes both DB records and physical orphaned image files).

## 🧠 System Architecture

The core processing logic follows a highly optimized pipeline:
`Video Input` ➔ `YOLOv11 (Detection)` ➔ `ByteTrack (Tracking)` ➔ `Size & Class Filter` ➔ `Time-Based Cropping` ➔ `Ollama VLM (Semantic Extraction)` ➔ `SQLite (Storage)`

## 🛠️ Tech Stack
- **AI / Computer Vision:** Ultralytics (YOLOv11), ByteTrack, OpenCV, Ollama (Qwen 2.5 Vision).
- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic.
- **Frontend:** React, TypeScript, Vite, TailwindCSS, Lucide Icons.

## 🚀 Getting Started (Local Development)

### Prerequisites
- Python 3.11+
- Node.js (v18+)
- [Ollama](https://ollama.com/) installed and running locally.

### 1. Model Setup
Pull the required Vision model using Ollama:
`ollama run qwen2.5vl:3b`

### 2. Backend Setup
`git clone https://github.com/USERNAME/vision-intelligence.git`
`cd vision-intelligence`
`uv venv`
`source .venv/bin/activate`
`uv pip install -r requirements.txt`
`uv run uvicorn backend.main:app --reload`

### 3. Frontend Setup
`cd frontend`
`npm install`
`npm run dev`

## 📸 Screenshots
*(TBD: Add your screenshots of the Dashboard, Semantic Search, and Lightbox here!)*

---
*Developed as a showcase of end-to-end System Design and AI Integration.*
