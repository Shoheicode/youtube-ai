
# 🧠 Full-Stack Application

This project features a Python backend server and a Next.js frontend. Follow the instructions below to set up and run the application locally.

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
