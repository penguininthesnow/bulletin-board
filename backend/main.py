from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection
from s3 import upload_image

from fastapi.staticfiles import StaticFiles

app = FastAPI()


# 讓前端fetch 不會被擋
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# # 暫存留言 RDS
# messages = []


@app.post("/api/messages")
async def create_message(content: str = Form(...), image: UploadFile = File(...)):
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


# 靜態網頁
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
