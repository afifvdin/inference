from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from app.core.settings import settings
from app.core.state import State
from app.routes.pos_tagger import pos_tagger_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.state = State()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(pos_tagger_router)


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    if not app.openapi_url:
        raise ValueError("openapi_url is None")

    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
