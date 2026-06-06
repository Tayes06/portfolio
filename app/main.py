import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.config import settings
from app.database import init_db, engine
from app.routes import pages, cv, rag_api, anomaly_api, n8n_api
from app.i18n import Translator, AVAILABLE_LANGUAGES

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"), cache_size=0)


def render(name: str, request: Request, context: dict | None = None):
    lang = request.cookies.get("lang", "en")
    translator = Translator(lang)
    ctx = {
        "request": request,
        "t": translator.t,
        "current_lang": lang,
        "available_languages": AVAILABLE_LANGUAGES,
    }
    if context:
        ctx.update(context)
    return templates.TemplateResponse(name, ctx)


# Share the configured templates and render helper with route modules
pages.render = render
import app.routes.pages as pages_module
pages_module.render = render

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

app.include_router(pages.router)
app.include_router(cv.router)
app.include_router(rag_api.router)
app.include_router(anomaly_api.router)
app.include_router(n8n_api.router)


@app.post("/api/lang")
async def set_language(request: Request):
    data = await request.json()
    lang = data.get("lang", "en")
    from fastapi.responses import JSONResponse
    response = JSONResponse({"lang": lang})
    response.set_cookie(key="lang", value=lang, max_age=365 * 24 * 3600, path="/")
    return response
