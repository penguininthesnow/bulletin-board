from fastapi import FastAPI, UploadFile, Form
from database import get_connection
from s3 import upload_image

app = FastAPI()


@app.post("/api/messages")
async def create_message(content: str = Form(...), image: UploadFile = Form(...)):
    image_url = upload_image(image)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (content, image_url) VALUES (%s, %s)",
        (content, image_url),
    )
    conn.commit()

    return {"ok": True}


@app.get("/api/messages")
def get_messages():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM messages ORDER BY created_at DESC")
    return cursor.fetchall()
