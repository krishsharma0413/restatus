# region [imports]
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core import html_writter, updater

# endregion
# region [variables]

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
updater()

# endregion

# region [HTML]

@app.get("/", response_class=HTMLResponse)
def index(requests: Request):
    renderall = html_writter()
    return templates.TemplateResponse("index.html",{"request":requests, "status_page_content": renderall[1], "asc": renderall[0], "operational": renderall[2]})

@app.get("/uptimebot")
def uptimebot(requests: Request):
    """
    due to replit shutting down its repl if no activity,
    this is a workaround to keep it running 
    """
    return "uptimebot my beloved"

# endregion