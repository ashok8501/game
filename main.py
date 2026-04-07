from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import get_connection
from flames_logic import calculate_flames




app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/calculate", response_class=HTMLResponse)
def calculate(request: Request, boy: str = Form(...), girl: str = Form(...)):
    result = calculate_flames(boy, girl)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO flames_results (boy_name, girl_name, result) VALUES (%s, %s, %s)",
        (boy, girl, result)
    )

    conn.commit()
    cur.close()
    conn.close()

    return templates.TemplateResponse("result.html", {
        "request": request,
        "boy": boy,
        "girl": girl,
        "result": result
    })


@app.get("/history", response_class=HTMLResponse)
def history(request: Request):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT boy_name, girl_name, result FROM flames_results ORDER BY id DESC")
    data = cur.fetchall()

    cur.close()
    conn.close()

    return templates.TemplateResponse("history.html", {
        "request": request,
        "records": data
    })