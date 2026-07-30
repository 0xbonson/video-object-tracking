# Video Person Tracking & Semantic Attribute Extraction

A local-first Computer Vision pipeline that tracks individuals in video footage and extracts their semantic attributes (e.g., gender, clothing color, outfit type) using Vision Language Models (VLM).

Built to solve the challenge of cataloging dynamic subjects in videos (like tracking the main artist in a fancam), this system isolates primary subjects, samples frames efficiently, and structures the output for semantic search.

## Engineering Highlights

*   **Area-Based Subject Isolation:** Instead of tracking every detected person, the YOLOv11 pipeline filters out background crowds by setting a >15% bounding box area threshold.
*   **Time-Based Frame Sampling:** To prevent VLM bottlenecking and database bloat, tracked IDs are sampled every 3 seconds to capture wardrobe transitions (the "OOTD" tracking logic).
*   **Constraining VLM Outputs:** Uses local `qwen2.5vl:3b` via Ollama with strict prompt constraints and `temperature=0.0` to force deterministic JSON formats and reduce visual hallucinations.
*   **Storage Garbage Collection:** The React frontend includes a cleanup system that synchronizes database record deletions with the physical removal of cropped image files on the backend.

## System Architecture

Video Input -> YOLOv11 (Detection) -> ByteTrack -> Size/Class Filter -> Time-Based Crop -> Ollama (VLM) -> SQLite -> React Dashboard

## Tech Stack
*   **Computer Vision:** Ultralytics (YOLOv11), ByteTrack, OpenCV, Ollama (Qwen 2.5 Vision)
*   **Backend:** Python 3.11, FastAPI, SQLAlchemy, SQLite
*   **Frontend:** React, TypeScript, Vite, TailwindCSS

## Local Development Setup

### 1. Prerequisites
* Python 3.11+
* Node.js (v18+)
* Ollama installed locally.

### 2. Run the VLM
```bash
ollama run qwen2.5vl:3b
