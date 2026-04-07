from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import get_connection

app = FastAPI()

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# ✅ AUTO CREATE TABLE
@app.on_event("startup")
def create_table():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flames_data (
                id SERIAL PRIMARY KEY,
                boy_name TEXT,
                girl_name TEXT,
                result TEXT
            );
        """)

        conn.commit()
        cursor.close()
        conn.close()

        print("✅ Table ready")

    except Exception as e:
        print("❌ DB ERROR:", e)


# 🔥 FLAMES LOGIC
def flames_result(name1, name2):
    name1 = name1.lower().replace(" ", "")
    name2 = name2.lower().replace(" ", "")

    for ch in name1[:]:
        if ch in name2:
            name1 = name1.replace(ch, "", 1)
            name2 = name2.replace(ch, "", 1)

    count = len(name1 + name2)

    flames = ["Friends", "Love", "Affection", "Marriage", "Enemy", "Siblings"]

    while len(flames) > 1:
        index = (count % len(flames)) - 1

        if index >= 0:
            flames = flames[index+1:] + flames[:index]
        else:
            flames.pop()

    return flames[0]


# 🏠 HOME PAGE
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 📩 SUBMIT FORM
@app.post("/submit", response_class=HTMLResponse)
def submit(request: Request, boy_name: str = Form(...), girl_name: str = Form(...)):
    try:
        result = flames_result(boy_name, girl_name)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO flames_data (boy_name, girl_name, result) VALUES (%s, %s, %s)",
            (boy_name, girl_name, result)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return templates.TemplateResponse("result.html", {
            "request": request,
            "boy_name": boy_name,
            "girl_name": girl_name,
            "result": result
        })

    except Exception as e:
        return {"error": str(e)}


# 📊 VIEW DATA
@app.get("/data")
def get_data():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM flames_data")
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    except Exception as e:
        return {"error": str(e)}