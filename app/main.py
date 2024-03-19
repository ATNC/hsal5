from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastui import prebuilt_html

from .database.init_db import init_db
from .routers import currency

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    init_db()
    print("Database initialized.")

app.include_router(currency.router)


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """
    Simple HTML page which serves the React app, comes last as it matches all paths.
    """
    return HTMLResponse(prebuilt_html(title='Currency'))
