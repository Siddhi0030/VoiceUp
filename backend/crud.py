import json
from db import get_connection

def clear_and_insert():
    with open("backend/mock_conversations.json", "r") as f:
        data = json.load(f)

    conn = get_connection()
    cursor = conn.cursor()

    print("Clearing old data...")
    cursor.execute("DELETE FROM analysis_results")
    cursor.execute("DELETE FROM messages")
    cursor.execute("DELETE FROM conversations")
    conn.commit()

    # Reset ID counters
    cursor.execute("ALTER TABLE conversations AUTO_INCREMENT = 1")
    cursor.execute("ALTER TABLE messages AUTO_INCREMENT = 1")
    cursor.execute("ALTER TABLE analysis_results AUTO_INCREMENT = 1")


    print("Inserting new mock data...")
    for convo in data:
        cursor.execute("INSERT INTO conversations () VALUES ()")
        conversation_id = cursor.lastrowid

        for msg in convo["messages"]:
            cursor.execute(
                "INSERT INTO messages (conversation_id, sender, text) VALUES (%s, %s, %s)",
                (conversation_id, msg["sender"], msg["text"])
            )

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Done! Database is ready with mock conversations.")

if __name__ == "__main__":
    clear_and_insert()
