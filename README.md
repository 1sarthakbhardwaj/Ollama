
# Local Mini DeepSeek with Qwen3 & Ollama

This project leverages **Qwen3:4B** and **Ollama** inference to create a 100% local ChatGPT-like app with a hybrid thinking UI built on Streamlit.

---

## 🚀 Installation and Setup

### 1. Setup Ollama
```bash
# Install Ollama on Linux
curl -fsSL https://ollama.com/install.sh | sh
# Pull the Qwen3:4B model
ollama pull qwen3:4b
```

### 2. Install Python Dependencies
```bash
pip install streamlit ollama
```

---

## ▶️ Running the App
```bash
streamlit run app.py
```

---

## ✨ Features
- **Local inference** using Ollama and Qwen3
- **Hybrid Thinking UI**: enable `/think` mode to reveal chain-of-thought steps
- **Toggle reasoning** on/off directly in the chat input

---

## 🗂 Project Structure
```bash
.
├── assets/
│   ├── logo_qwen3.png
│   └── ollama.jpg
├── app.py
└── README.md
```

---

## 📝 Usage
1. Launch the app with `streamlit run app.py`.
2. Toggle **Enable step-by-step reasoning 🧠** at the bottom.
3. Type your question in the input box and press Enter.
4. View answer with or without chain-of-thought.


