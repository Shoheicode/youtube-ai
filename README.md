
# 🎥 YouTube-AI Project

**YouTube Highlight Summarizer** is an AI-powered tool that fetches and analyzes the most recent YouTube appearance of a given person (e.g., "Howard Marks, leading US investor") and generates:

- ✍️ Up to **5 key highlights** summarizing the content (max 250 words total)
- 🎬 A **20-second video clip** attached to each highlight

---

## 🧠 How It Works

1. **Input**: The user provides a prompt identifying a person (e.g., name + context).
2. **Search**: The app uses the **YouTube Data API** to find their latest public appearance.
3. **Transcribe**: The selected video is transcribed using **OpenAI Whisper**.
4. **Summarize**: The transcription is segmented and summarized using **GPT**.
5. **Clip**: The app automatically extracts relevant 20-second video clips for each highlight.
6. **Output**: A clean summary + video clips are presented via the frontend.

---
## 🛠 Tech Stack
- **Frontend**: Next.js (Vercel deployment)
- **Backend**: Node.js / Python API (for Whisper + processing)
- **APIs**:
  - [YouTube Data API](https://developers.google.com/youtube/v3)
  - [OpenAI Whisper](https://github.com/openai/whisper) for transcription
  - [OpenAI GPT](https://platform.openai.com/docs/guides/gpt) for summarization
- **Video Processing**: `ffmpeg` for trimming video segments

---

## 🚀 Getting Started

### 🔧 Prerequisites

Make sure you have the following installed:

- [Python 3](https://www.python.org/downloads/)
- [Node.js & npm](https://nodejs.org/)
- (Optional) [Yarn](https://yarnpkg.com/), [pnpm](https://pnpm.io/), or [Bun](https://bun.sh/)

---

## 🐍 Running the Python Backend

### 1. Navigate to the Python backend directory:
```bash
cd PythonServer
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the backend server:
```bash
# For Python 3
python3 app.py

# Or if python points to Python 3
python app.py
```
The backend will be running on [http://localhost:8000](http://localhost:8000) by default.

---

## 🌐 Running the Next.js Frontend

### 1. Navigate to the frontend project directory:
(Assuming it's in the root or in a separate directory like `frontend`)

```bash
cd path/to/frontend
```

### 2. Install frontend dependencies:
```bash
npm install
# or
yarn
# or
pnpm install
# or
bun install
```

### 3. Start the development server:
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

The app will be running on [http://localhost:3000](http://localhost:3000) by default.

---

## 📁 Project Structure

```
root/
│
├── PythonServer/         # Python backend
│   ├── app.py            # Entry point for backend server
│   └── requirements.txt  # Python dependencies
│
└── frontend/             # Next.js frontend (rename if needed)
    ├── package.json
    └── ...
```

---

## 💬 Contributing

Feel free to open issues or pull requests to improve this project!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
