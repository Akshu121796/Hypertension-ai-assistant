# Hypertension-ai-assistant

> An intelligent and friendly AI chatbot that helps users understand and manage **hypertension (high blood pressure)** using the power of **Google Gemini AI** — all wrapped in a beautiful Streamlit interface.

---

## 🌟 Features

✅ **Interactive Chat Interface** – Talk with an AI assistant specialized in hypertension.  
✅ **Real-Time AI Responses** – Uses Gemini API for reliable, grounded information.  
✅ **Health-Focused Design** – Offers lifestyle tips and explanations for hypertension care.  
✅ **Smart Suggestions** – Quick-access buttons for common questions.  
✅ **Attractive Frontend UI** – Stylish chat bubbles, gradient colors, and smooth layout.  
✅ **Custom CSS Styling** – Fully customizable design via `gui_style.css`.  
---

## 🛠️ Tech Stack

| Component | Technology |
|------------|-------------|
| 💬 Chat Logic | Python + Streamlit |
| 🧩 AI Model | Google Gemini API (Generative Language API) |
| 🎨 Frontend | Streamlit + Custom CSS |
| 📦 Dependencies | `requests`, `streamlit`, `json`, `time` |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Akshu121796/Hypertension-ai-assistant.git
cd Hypertension-ai-assistant
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure API Key

Inside your `.streamlit/secrets.toml` file, add:

```toml
GEMINI_API_KEY = "your_google_api_key_here"
```

### 5️⃣ Run the App

```bash
streamlit run app.py
```

## 🖌️ File Structure

```
HeartWise-AI/
│
├── app.py                # Main Streamlit application
├── gui_style.css         # Chat UI styling
├── requirements.txt      # Python dependencies
├── .streamlit/
│   └── secrets.toml      # Gemini API key (private)
├── docs/
│   └── demo_screenshot.png
└── README.md
```

---

## 💡 Example Questions You Can Ask

* What are the symptoms of hypertension?
* How can I naturally reduce my blood pressure?
* What foods should I avoid if I have high BP?
* Can hypertension be cured permanently?
* How does stress affect blood pressure?

---

## ⚠️ Disclaimer

> This chatbot provides **AI-generated educational information** and **not medical advice**.
> Always consult a qualified healthcare professional for diagnosis or treatment.

---

## ⭐ Contribute

Feel free to  fork in!!!
---

