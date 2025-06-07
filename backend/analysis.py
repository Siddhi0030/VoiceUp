import io
import base64
import json
import re
import matplotlib
import requests
import matplotlib.pyplot as plt
from matplotlib import cm
from transformers import pipeline
from collections import Counter
matplotlib.use('Agg')

OPENROUTER_API_KEY = "your-api-key"

# Load sentiment analysis model
emotion_model = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

def analyze_emotions(messages):
    return [
        {
            "sender": msg["sender"],
            "text": msg["text"],
            "emotion": emotion_model(msg["text"])[0]
        }
        for msg in messages
    ]

def check_compliance(conversation):
    rules = [
        "1. Greet the customer at the beginning.",
        "2. Apologize if the customer expresses frustration or anger.",
        "3. Confirm resolution before ending the chat.",
        "4. Avoid making unsupported claims.",
        "5. Personalize the chat by using customer's name."
    ]
    chat = "\n".join([f"{m['sender']}: {m['text']}" for m in conversation])
    prompt = f"""
    You are a customer support compliance assistant.

    Check if the **AGENT** followed the appropriate rules during this chat.

    ### Compliance Rules:
    1. Greet the customer at the beginning (if applicable).
    2. Apologize if the customer expresses frustration or anger.
    3. Confirm resolution if the customer reported an issue.
    4. Avoid making unsupported claims (e.g., "guaranteed fix").
    5. Personalize the chat using the customer's name if known.

    ### Instructions:
    - Only evaluate rules that are **relevant** based on the conversation.
    - For each rule, return:
    - `true` if followed
    - `false` if relevant but not followed
    - `"not_applicable"` if the rule doesn't apply to this conversation
    - Then return an overall `score` (0-100) **based only on relevant rules**.

    ### Format:
    Respond ONLY with valid JSON like this:
    {{
    "rule_1": true,
    "rule_2": "not_applicable",
    "rule_3": "not_applicable",
    "rule_4": true,
    "rule_5": true,
    "score": 100
    }}

    ### Conversation:
    {chat}
    """


    # Call OpenRouter API to analyze compliance
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/gemma-3-27b-it:free",  # or "zephyr", etc.
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    try:
        content = response.json()["choices"][0]["message"]["content"]
        json_text = re.search(r"\{.*\}", content, re.DOTALL).group(0)
        return json.loads(json_text)
    except:
        return {"error": "Failed to parse", "raw": response.text}


def generate_emotion_chart(emotions):
    emotion_counts = Counter([e["emotion"]["label"] for e in emotions])
    fig, ax = plt.subplots(figsize=(5, 5))

    wedges, texts, autotexts = ax.pie(
        emotion_counts.values(),
        labels=emotion_counts.keys(),
        autopct='%1.1f%%',
        startangle=140,
        colors=cm.Set3.colors
    )
    ax.set_title("Emotion Distribution", fontsize=14)
    plt.setp(autotexts, size=10, weight="bold")

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf