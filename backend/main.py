from fastapi import FastAPI
from backend.db import get_connection
from backend.analysis import analyze_emotions, check_compliance
from fastapi.responses import StreamingResponse
from backend.analysis import generate_emotion_chart
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/conversations")
def get_conversations():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM conversations")
    conversations = cursor.fetchall()

    result = []
    for convo in conversations:
        cursor.execute("SELECT sender, text FROM messages WHERE conversation_id = %s", (convo["id"],))
        messages = cursor.fetchall()
        result.append({
            "conversation_id": convo["id"],
            "messages": messages
        })

    cursor.close()
    conn.close()
    return result

@app.get("/analysis/{conversation_id}")
def analyze_conversation(conversation_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT sender, text FROM messages WHERE conversation_id = %s", (conversation_id,))
    messages = cursor.fetchall()
    cursor.close()
    conn.close()

    emotions = analyze_emotions(messages)
    compliance_result = check_compliance(messages)

    return {
        "conversation_id": conversation_id,
        "emotions": emotions,
        "compliance_score": compliance_result
    }

@app.get("/chart/{conversation_id}")
def emotion_chart(conversation_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT sender, text FROM messages WHERE conversation_id = %s", (conversation_id,))
    messages = cursor.fetchall()
    cursor.close()
    conn.close()

    from backend.analysis import analyze_emotions
    emotions = analyze_emotions(messages)

    chart_buf = generate_emotion_chart(emotions)
    return StreamingResponse(chart_buf, media_type="image/png")
