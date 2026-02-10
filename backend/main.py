from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import get_connection
from s3 import upload_image
import pymysql


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "https://www.penguinthesnow.com",
        "https://penguinthesnow.com",
        "http://18.234.62.161",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# POST 資料上傳
@app.post("/api/messages")
async def create_message(content: str = Form(...), image: UploadFile = File(None)):

    image_url = None
    if image:
        image_url = upload_image(image)  # 用 S3  回傳的 URL

    conn = get_connection()
    cursor = conn.cursor()
    # 存進資料庫
    cursor.execute(
        "INSERT INTO messages (content, image_url) VALUES (%s, %s)",
        (content, image_url),
    )
    conn.commit()

    return {"ok": True}


# GET API
@app.get("/api/messages")
def get_messages():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM messages ORDER BY id DESC")
    return cursor.fetchall()


app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")


# =============================================================

# 讓前端fetch 不會被擋
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "https://www.penguinthesnow.com",
#         "https://d1alcb35jz82s5.cloudfront.net",
#         # "https://penguinthesnow.com",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # 暫存留言 RDS
# messages = []

# # GET 資料回傳
# @app.get("/api/messages")
# def get_messages():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM messages ORDER BY created_at DESC")
#     return list(cursor.fetchall())


# # 靜態網頁
# app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


# @app.post("/api/messages")
# async def create_message(content: str = Form(...), image: UploadFile = File(...)):
#     file_path = f"uploads/{image.filename}"
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(image.file, buffer)

#     image_url = f"/uploads/{image.filename}"
