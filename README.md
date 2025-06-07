
---

# 📊 VoiceUp AI Analytics Dashboard

A smart AI-powered system to analyze customer support conversations for:
- 🎭 Emotion Detection
- ✅ Compliance Checking
- 📈 Visual Reporting

---

## 🚀 Features

- 💬 Shows agent vs. customer messages with detected emotions
- 🧠 Uses **Transformers** for emotion analysis
- ✅ Uses **open-source LLM (via API)** for compliance rule evaluation
- 📊 Generates emotion distribution charts
- 🧪 Rules are dynamically evaluated (only if applicable)
- 🌙 Beautiful dark mode frontend

---

## 🧱 Tech Stack

| Layer         | Technology |
|---------------|------------|
| **Frontend**  | HTML, CSS (Dark Theme), JavaScript, Bootstrap |
| **Backend**   | FastAPI (Python) |
| **AI Models** | HuggingFace Transformers (emotion) + OpenRouter LLM API (compliance) |
| **LLM Model** | `google/gemma-3-27b-it:free` (hosted via OpenRouter.ai) |
| **Database**  | MySQL |
| **Visualization** | Matplotlib |

---

## 📦 Installation & Setup

### 1. Clone Repo

```bash
git clone https://github.com/Siddhi0030/VoiceUp
cd VoiceUp
````

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note:** Requires Python 3.10+ and MySQL server running locally.

### 3. Configure MySQL

* Create a database called `voiceup`
* Import the provided schema (if applicable)

### 4. Add `.env` or Config File

Store your [OpenRouter API key](https://openrouter.ai) here:

```env
OPENROUTER_API_KEY=your-key-here
```

Or directly paste the key in `analysis.py` where required.

---

## 🖥️ Running the App

### Start Backend (FastAPI)

```bash
uvicorn backend.main:app --reload
```

### Open Frontend

Open `frontend/index.html` in your browser. Make sure CORS is enabled in FastAPI if needed.

---

## 💡 How It Works

### 1. User selects a conversation

### 2. Backend:

* Fetches messages from DB
* Runs **emotion detection** using HuggingFace Transformers
* Sends full conversation to **LLM** for compliance analysis

  * LLM returns per-rule result + dynamic score
  * Skips rules when not applicable (e.g., no apology needed if no issue)
* Sends JSON response to frontend

### 3. Frontend:

* Displays chat with emotion tags
* Lists compliance result (✅ / ❌ / ➖)
* Shows a pie chart of emotion distribution

---

## ✅ Compliance Rules Evaluated

1. Greet the customer at the beginning
2. Apologize if the customer expresses frustration
3. Confirm resolution if an issue was reported
4. Avoid making unsupported claims
5. Personalize the conversation (use customer's name)

---
